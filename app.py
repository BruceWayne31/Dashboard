import streamlit as st
import pandas as pd
from methods import *
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from methods import *
from DB_methods import *
import datetime
m=methods()
dm=db_methods()
st.set_page_config(page_title="Dashboard",page_icon=":bar_chart:",layout="wide")
Type=st.sidebar.selectbox("Select the level of the dashboard",options=["Account","Project"])
acc_data,Names,acc_level_competencies,acc_data_dic=m.acc_level_data()

if Type=="Account":
    st.title(":bar_chart: Competency Tracker")
    choice=st.selectbox("How may I assist",options=["","View Competency Dashboard","Assign Deadlines"])
    if choice=="View Competency Dashboard":
        st.markdown("##")
        
        
        #KPIs#
        No_of_competencies=len(acc_level_competencies)
        team=acc_data.groupby(acc_data.columns.tolist()[2]).count().index.tolist()
        count=acc_data.groupby(acc_data.columns.tolist()[2]).count()[acc_data.columns.tolist()[0]].tolist()
        index=count.index(max(count))
        max_team=team[index]
        comp=acc_data.groupby(acc_data.columns.tolist()[6]).count().index.tolist()
        comp_count=acc_data.groupby(acc_data.columns.tolist()[6]).count()[acc_data.columns.tolist()[0]].tolist()
        comp_index=comp_count.index(max(comp_count))
        max_comp=comp[comp_index]
        left,center,right=st.columns(3)
        with left:
            st.subheader("No of competency monitored")
            st.write(f"{No_of_competencies}")
        with center:
            st.subheader("Team with maximum defaulters")
            st.write(f"{max_team}")
        with right:
            st.subheader("Competency with maximum defaults" )
            st.write(f"{max_comp}: {max(comp_count)} defaulters ")
        st.markdown("---")
        
        
        numbers=[]
        for i in acc_level_competencies:
            numbers.append(acc_data[acc_data["Defaulting Competency"]==i][acc_data.columns.tolist()[0]].count().tolist())
        fig=px.bar(x=acc_level_competencies,y=numbers,title="Competency wise defaulter count")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        fig.update_traces(width=0.5)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("---")
        team_name=acc_data[acc_data.columns.tolist()[2]].unique().tolist()
        comp_name=st.selectbox("Select the competency",options=acc_level_competencies)
        
        team_name=acc_data[acc_data["Defaulting Competency"]==comp_name].groupby(acc_data.columns.tolist()[2]).count().index.tolist()
        team_number=acc_data[acc_data["Defaulting Competency"]==comp_name].groupby(acc_data.columns.tolist()[2]).count()[acc_data.columns.tolist()[0]].tolist()
        if len(team_name )== 0:
            st.markdown("##")
            st.markdown("##")
            
            st.write("No defaulters for this course across the teams")
        else:
            fig=px.bar(x=team_number,y=team_name,color=team_name,title=f"Teamwise distribution of defaulters for {comp_name}")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",height=500)
            fig.update_traces(width=0.5)
            st.plotly_chart(fig,use_container_width=True)
        tn=st.selectbox("Select the team name",options=team_name)
        
        left2,right2=st.columns(2)
        with left2:
            
            st.markdown("##")
            st.markdown("##")
            df3=acc_data[(acc_data["Defaulting Competency"]==comp_name)]
            df4=df3[df3["Team"] == tn]
            st.markdown("##")
            st.write(f"Defaultig employees for {tn} ")
            st.dataframe(df4[df4.columns.tolist()[:5]])
            pcount=len(df4["Emp ID"].values.tolist())
            pcount_name=len(Names[Names["Team"]==tn]["Emp ID"].values.tolist())
            dfp2=pd.DataFrame({"comps2":[pcount,pcount_name-pcount],"att2":["defaulters","non-defaulters"]})
        with right2:
            st.markdown("##")
            st.markdown("##")
            df3=acc_data[(acc_data["Defaulting Competency"]==comp_name)]
            df4=df3[df3["Team"] == tn]
            
            pcount=len(df4["Emp ID"].values.tolist())
            pcount_name=len(Names[Names["Team"]==tn]["Emp ID"].values.tolist())
            dfp2=pd.DataFrame({"comps2":[pcount,pcount_name-pcount],"att2":["defaulters","non-defaulters"]})
            fig5=px.pie(dfp2,values="comps2",names="att2",title=f"Defaulter percentage in {comp_name} for {tn}")
            fig5.update_layout(plot_bgcolor="rgba(0,0,0,0)",height=400)
            st.plotly_chart(fig5,use_container_width=True)
            
        st.markdown("---")    
        Name_list=Names[Names["Team"]==tn]["Name of the Resources"].tolist()
        numbers2=[]
        for i in Name_list:
            numbers2.append(acc_data[acc_data[acc_data.columns.tolist()[1]]==i][acc_data.columns.tolist()[0]].count().tolist())
        fig=px.bar(x=numbers2,y=Name_list,color=Name_list,title=f"Number of defaults for each member of {tn} ")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        fig.update_traces(width=0.5)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("---")
        emp_name=st.selectbox("Select the name of the employee",options=Name_list)
        EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
        emp_competencies=acc_data[acc_data[acc_data.columns.tolist()[1]]==emp_name][acc_data.columns.tolist()[6]]
        dates_list=[]
        for i in emp_competencies:
            c=dm.get_date(EmpID, i)
            if len(c)==0:
                dates_list.append(" ")  
            else:
                dates_list.append(c[0][0])
        t=[]
        for i in emp_competencies:
           t.append(acc_data[(acc_data["Defaulting Competency"]==i) & (acc_data["Name of the Resources"]==emp_name)]["Required"].tolist()[0])
            
        df2=pd.DataFrame({"Competecny":emp_competencies,"Next Milestone":t,"Due Date":dates_list})
        def date_diff(date1, date2):
            return (date1 - date2).days
        def check_closest_expiring_date(dates):
            todays_date = datetime.date.today()
            minimum = 999999
            closest_expiring_date_and_index = {"Closest Expiring Date":[], "Closest Expiring Date Index":[]}
            for i in range(len(dates)):
                if dates[i] not in [None, '', ' ', "", " "]:
                    if dates[i] > todays_date:
                        diff = date_diff(dates[i], todays_date)
                        if diff < minimum:
                            minimum = diff
                            closest_expiring_date_and_index["Closest Expiring Date"] = dates[i]
                            closest_expiring_date_and_index["Closest Expiring Date Index"] = i
            return closest_expiring_date_and_index
        def check_if_date_has_expired(dates):
            expired_dates_and_index = {"Expired Dates":[], "Expired Dates Index":[]}
            todays_date = datetime.date.today()
            #print("TODAY'S DATE \n", todays_date)
            for i in range(len(dates)):
                if dates[i] not in [None, '', ' ',"", " "]:
                    if dates[i] < todays_date:
                        expired_dates_and_index["Expired Dates"].append(dates[i])
                        expired_dates_and_index["Expired Dates Index"].append(i)
            return expired_dates_and_index
        def string_to_datetime(date_list):
            format = "%Y-%m-%d"
            dates=[]
            for i in date_list:
                if i in [None, '', ' ', "", " "]:
                    dates.append(i)
                else:
                    #print(datetime.datetime.strptime(i, format).date())
                    dates.append(datetime.datetime.strptime(i, format).date())
            return dates
        string_to_datetime(dates_list)
        dates = string_to_datetime(dates_list)
        #print("CONVERTED TO DATES\n", dates)
        expired_dates_and_index = check_if_date_has_expired(dates)
        #print("EXPIRED DATES INDEX \n", expired_dates_and_index)
        expired_index = expired_dates_and_index["Expired Dates Index"]
        expired_date_count = len(expired_dates_and_index["Expired Dates"])
        print("Indexes: ", expired_index," Expired date count: ",expired_date_count)
        closest_expiring_date_and_index = check_closest_expiring_date(dates)
        #print(closest_expiring_date_and_index)
        closest_expiring_date = closest_expiring_date_and_index["Closest Expiring Date"]
        closest_expiring_date_index = closest_expiring_date_and_index[ "Closest Expiring Date Index"]
        print("Closes Expiring Date: ", closest_expiring_date, " Index of closest expiring date :", closest_expiring_date_index)
        left3,center3,right3=st.columns((2,2,1))
        with left3:
            st.write(f"{emp_name}'s deadlines")
            st.markdown("##")
            st.markdown("##")
            
            st.dataframe(df2)
        with center3:
            st.write("Levels of competency required to achieve target")
            levels=acc_data[acc_data["Name of the Resources"]==emp_name]["Required"].tolist()
            levels_unique=acc_data[acc_data["Name of the Resources"]==emp_name]["Required"].unique()
            cl=[]
            for i in levels_unique:
                cl.append(levels.count(i))
            if len(cl) != 0:
                fig=px.bar(x=cl,y=levels_unique)
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)" , width=200,height=300)
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.write("Target already met")
        with right3:
            st.write("      "+"Employee Details")
            st.markdown("##")
            st.markdown("##")
            
            st.write("      "+f"Number of defaulting courses: {len(emp_competencies)}")
            c=(len(emp_competencies)/len(acc_level_competencies))*100
            st.write("      "+f"Defaulting percentage: {round(c,2)}%")
            st.write(f"number of defaulted dates: {len(expired_index)}")
            st.write("Overdue competencies:")
            for i in expired_index:
                st.write(f"{emp_competencies.values.tolist()[i]}")
            if closest_expiring_date != []:   
                st.write(f"Nearest deadline: {closest_expiring_date} ")
            else:
                st.write(f"Nearest deadline: No Data Available")
            
    elif choice=="Assign Deadlines":
        
        team_name=acc_data[acc_data.columns.tolist()[2]].unique().tolist()
        tn=st.selectbox("Select the team name",options=team_name)
        n=Names[Names["Team"]==tn]["Name of the Resources"].tolist()
        st.title("Deadlines")
        st.header("Deadline Tracker")
        left,center,right,right1=st.columns(4)
        with left:
            emp_name=st.selectbox("name of the employee", n)
        c=0
        cr=[]
        for i in acc_data_dic:
            if emp_name in acc_data_dic[i][acc_data_dic[i].columns[1]].tolist():
                cr.append(i)
                c=c+1
        l=[]
        for j in n:
            x=0
            for i in acc_data_dic:
                if j in acc_data_dic[i][acc_data_dic[i].columns[1]].tolist():
                    
                    x=x+1
            l.append(x)
        
        with center:
            comp=st.selectbox("Competencies", cr)
        with right:
            if comp != None:
                req=acc_data_dic[comp][acc_data_dic[comp]["Name of the Resources"]==emp_name]["Required"].tolist()
                st.selectbox("Required competency", req)
                with right1:
                    date=st.date_input("Deadline for completion")
        if comp != None:
            EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
            chck=dm.check_record(EmpID, emp_name, comp, date)
            if len(chck)==0:
                button=st.button("Assign deadline")
            else:
                button=st.button("Update deadline")
            if button==True:
                EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
                c=dm.create_record(EmpID, emp_name, comp, date)
                st.write(c)
elif Type=="Project":
    team_name2=acc_data[acc_data.columns.tolist()[2]].unique().tolist()
    
    ch=st.sidebar.selectbox("Select the team",options=team_name2)
    data_dic,counts,headings,competencies,Names=m.dataframe(ch)
    if data_dic != "":
        st.markdown("##")
        st.title(":bar_chart: Competency Tracker")
        ncomp=len(competencies)
        nemp=Names[Names.columns[0]].count()
        maximum=max(list(counts))
        ind=list(counts).index(maximum)
        max_defaulters=list(competencies)[ind]
        choice=st.selectbox("How may I Assist you", ["","View Competency Dashboard","Assign Deadlines"]) 
        if choice=="View Competency Dashboard":
            left,center,right=st.columns(3)
            with left:
                st.subheader("Total number of competencies")
                st.subheader(ncomp)
            with center:
                st.subheader("Total number of employees")
                st.subheader(nemp)
            with right:
                st.subheader("maximum defaulters")
                st.subheader(f"{max(counts)} : {max_defaulters}")
            st.markdown("---")
            
        
            
            
            n=Names[Names.columns[1]].tolist()
            
            fig=px.bar(x=list(headings),y=list(counts),title="Number of defaulters for each competency")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("---")
            competency=st.selectbox("Select the competency",options=competencies)
            left1,right1=st.columns(2)
            c=0
            cr=[]
            l=[]
            for j in n:
                x=0
                for i in data_dic:
                    if j in data_dic[i][data_dic[i].columns[1]].tolist():
                        
                        x=x+1
                l.append(x)
            st.markdown("---")
            fig2=px.bar(x=n,y=l,title="Number of defaults by each employee")
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2,use_container_width=True)
            st.markdown("---")
            emp_name=st.selectbox("Select the Name of the employee",options=n,)
            
            with left1:
                
                cc=data_dic[competency]["Emp ID"].count()
                st.write(f"There are {cc} defaulters for {competency}")
                st.dataframe(data_dic[competency].drop(["Date","Gap"],axis=1))
            with right1:
                cc=data_dic[competency]["Emp ID"].count()
                dfp=pd.DataFrame({"comps":[int(cc),int(nemp)-int(cc)],"att":["defaulters","non-defaulters"]})
                fig3 = px.pie(dfp, values='comps',names='att',title=f"Defaulter percentage for {competency}")
                fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig3,use_container_width=True)
            
            
                
            
            
            for i in data_dic:
                if emp_name in data_dic[i][data_dic[i].columns[1]].tolist():
                    cr.append(i)
                    c=c+1
            
            
            left2,center2,right2=st.columns((2,2,1))
            with left2:
                st.write(f"{emp_name}'s deadlines")
                EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
                dates_list=[]
                for i in cr:
                    
                    
                    c=dm.get_date(EmpID, i)
                    if len(c)==0:
                        dates_list.append(" ")
                        
                    else:
                        dates_list.append(c[0][0])
                required=[]
                for i in cr:
                    required.append(data_dic[i][data_dic[i]["Name of the Resources"]==emp_name]["Required"].tolist()[0])
                df2=pd.DataFrame({"Competecny":cr,"Next Milestone": required,"Due Date":dates_list})
                st.dataframe(df2)
            with center2:
                required=[]
                for i in cr:
                    required.append(data_dic[i][data_dic[i]["Name of the Resources"]==emp_name]["Required"].tolist()[0])
                df2=pd.DataFrame({"Competecny":cr,"Next Milestone": required})
                unique=df2["Next Milestone"].unique()
                values=df2["Next Milestone"].values.tolist()
                count=[]
                for i in unique:
                    count.append(values.count(i))
                if len(count) !=0:
                    
                    fig2=px.bar(x=count,y=unique,title="Levels required to meet the target")
                    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",width=200,height=300)
                    st.plotly_chart(fig2,use_container_width=True)
                else:
                    st.write("This employee has completed the targets")
            with right2:
                dates_list=[]
                for i in cr:
                    
                    
                    c=dm.get_date(EmpID, i)
                    if len(c)==0:
                        dates_list.append(" ")
                        
                    else:
                        dates_list.append(c[0][0])
                def date_diff(date1, date2):
                    return (date1 - date2).days
                def check_closest_expiring_date(dates):
                    todays_date = datetime.date.today()
                    minimum = 999999
                    closest_expiring_date_and_index = {"Closest Expiring Date":[], "Closest Expiring Date Index":[]}
                    for i in range(len(dates)):
                        if dates[i] not in [None, '', ' ', "", " "]:
                            if dates[i] > todays_date:
                                diff = date_diff(dates[i], todays_date)
                                if diff < minimum:
                                    minimum = diff
                                    closest_expiring_date_and_index["Closest Expiring Date"] = dates[i]
                                    closest_expiring_date_and_index["Closest Expiring Date Index"] = i
                    return closest_expiring_date_and_index
                def check_if_date_has_expired(dates):
                    expired_dates_and_index = {"Expired Dates":[], "Expired Dates Index":[]}
                    todays_date = datetime.date.today()
                    #print("TODAY'S DATE \n", todays_date)
                    for i in range(len(dates)):
                        if dates[i] not in [None, '', ' ',"", " "]:
                            if dates[i] < todays_date:
                                expired_dates_and_index["Expired Dates"].append(dates[i])
                                expired_dates_and_index["Expired Dates Index"].append(i)
                    return expired_dates_and_index
                def string_to_datetime(date_list):
                    format = "%Y-%m-%d"
                    dates=[]
                    for i in date_list:
                        if i in [None, '', ' ', "", " "]:
                            dates.append(i)
                        else:
                            #print(datetime.datetime.strptime(i, format).date())
                            dates.append(datetime.datetime.strptime(i, format).date())
                    return dates
                string_to_datetime(dates_list)
                dates = string_to_datetime(dates_list)
                #print("CONVERTED TO DATES\n", dates)
                expired_dates_and_index = check_if_date_has_expired(dates)
                #print("EXPIRED DATES INDEX \n", expired_dates_and_index)
                expired_index = expired_dates_and_index["Expired Dates Index"]
                expired_date_count = len(expired_dates_and_index["Expired Dates"])
                print("Indexes: ", expired_index," Expired date count: ",expired_date_count)
                closest_expiring_date_and_index = check_closest_expiring_date(dates)
                #print(closest_expiring_date_and_index)
                closest_expiring_date = closest_expiring_date_and_index["Closest Expiring Date"]
                closest_expiring_date_index = closest_expiring_date_and_index[ "Closest Expiring Date Index"]
                print("Closes Expiring Date: ", closest_expiring_date, " Index of closest expiring date :", closest_expiring_date_index)
                st.write("Employee details")
                st.write(f"Number of defaulting courses: {len(cr)}")
                per=(int(len(cr))/int((ncomp)))*100
                st.write(f"Defaulting percentage: {round(per,2)}%")
                st.write(f"number of defaulted dates: {len(expired_index)}")
                st.write("Overdue competencies:")
                for i in expired_index:
                    st.write(f"{emp_competencies.values.tolist()[i]}")   
                if closest_expiring_date != []:
                    st.write(f"Nearest deadline: {closest_expiring_date} ")
                else:
                    st.write("Nearest deadline: No Data Available")
                
        
                
                        
            
                
        if choice=="Assign Deadlines":
            
            n=Names[Names.columns[1]].tolist()
            st.title("Deadlines")
            st.header("Deadline Tracker")
            left,center,right,right1=st.columns(4)
            with left:
                emp_name=st.selectbox("name of the employee", n)
            c=0
            cr=[]
            for i in data_dic:
                if emp_name in data_dic[i][data_dic[i].columns[1]].tolist():
                    cr.append(i)
                    c=c+1
            l=[]
            for j in n:
                x=0
                for i in data_dic:
                    if j in data_dic[i][data_dic[i].columns[1]].tolist():
                        
                        x=x+1
                l.append(x)
            
            with center:
                comp=st.selectbox("Competencies", cr)
            with right:
                if comp !=None:
                    req=data_dic[comp][data_dic[comp]["Name of the Resources"]==emp_name]["Required"].tolist()
                    st.selectbox("Required competency", req)
                    with right1:
                        date=st.date_input("Deadline for completion")
            if comp != None:
                EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
                chck=dm.check_record(EmpID, emp_name, comp, date)
                if len(chck)==0:
                    button=st.button("Assign deadline")
                else:
                    button=st.button("Update deadline")
                if button==True:
                    EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
                    c=dm.create_record(EmpID, emp_name, comp, date)
                    st.write(c)
    else:
        st.subheader(f"Sorry, No Data is available for {ch}'s project level competency")            
