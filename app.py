import streamlit as st
import pandas as pd
from methods import *
from DB_methods import *
import plotly.express as px
m=methods()
dm=db_methods()
data_dic,counts,headings,competencies,Names=m.dataframe()
st.set_page_config(page_title="Dashboard",page_icon=":bar_chart:",layout="wide")
st.markdown("##")
st.title(":bar_chart: Competency Tracker")
ncomp=len(competencies)
nemp=Names[Names.columns[0]].count()
maximum=max(list(counts))
ind=list(counts).index(maximum)
max_defaulters=list(competencies)[ind]
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
choice=st.selectbox("How may I Assist you", ["View Competency Dashboard","Assign Deadlines"])  
if choice=="View Competency Dashboard":
    competency=st.sidebar.selectbox(
             "Select the competency",
             options=competencies
     )
    n=Names[Names.columns[1]].tolist()
    emp_name=st.sidebar.selectbox(
             "Select the Name of the employee",
             options=n
     )
    left1,right1=st.columns(2)
    with left1:
        cc=data_dic[competency]["Emp ID"].count()
        st.write(f"There are {cc} defaulters for {competency}")
        st.dataframe(data_dic[competency].drop(["Date","Gap","Current"],axis=1))
    with right1:
        fig=px.bar(x=list(headings),y=list(counts))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
    st.markdown("---")
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
    left2,right2=st.columns(2)
    with left2:
        st.subheader(f"{emp_name} is defaulting in {c} competencies")
        EmpID=Names[Names[Names.columns[1]]==emp_name]["Emp ID"].tolist()[0]
        dates_list=[]
        for i in cr:
            
            
            c=dm.get_date(EmpID, i)
            if len(c)==0:
                dates_list.append(" ")
                
            else:
                dates_list.append(c[0][0])
        df2=pd.DataFrame({"Competecny":cr,"Due Date":dates_list})
        st.dataframe(df2)
        
                
    with right2:
        fig2=px.bar(x=n,y=l)
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2)
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
        
        req=data_dic[comp][data_dic[comp]["Name of the Resources"]==emp_name]["Required"].tolist()
        st.selectbox("Required competency", req)
    with right1:
        date=st.date_input("Deadline for completion")
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