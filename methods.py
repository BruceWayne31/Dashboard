class methods():
    def acc_level_data(self):
        import pandas as pd
        import numpy as np
        df1=pd.read_excel("VF_Account_Level_Competency_Tracker - Report Gen.xlsm",sheet_name="Role- Competency Mapping",skiprows=1)
        df2=pd.read_excel("VF_Account_Level_Competency_Tracker - Report Gen.xlsm",sheet_name="Role- Competency Mapping",skiprows=2)
        df2=df2.drop(0)
        acc_level_competencies=df1.columns.tolist()
        for i in range(len(acc_level_competencies)):
            if "Unnamed:" in acc_level_competencies[i]:
                acc_level_competencies[i]=" "
        while " " in acc_level_competencies:
            acc_level_competencies.remove(" ")
        Names=df2[df2.columns.tolist()[:3]]
        df2=df2.drop(df2.columns.tolist()[:4],axis=1)
        acc_data_dic={}
        data=[]
        for i in range(3,len(df2.columns.tolist())+1,3):
            data.append(df2[df2.columns.tolist()[i-3:i]])
        for i in range(len(data)):
            data[i]=data[i].rename(columns={data[i].columns.tolist()[0]:"Required"})
            data[i]=data[i].rename(columns={data[i].columns.tolist()[1]:"Current"})
            data[i]=data[i].rename(columns={data[i].columns.tolist()[2]:"Gap"})
        for i in range(len(data)):
            data[i]=pd.concat([Names,data[i]],axis=1)
        for i in range(len(acc_level_competencies)):
            acc_data_dic[acc_level_competencies[i]]=data[i]
        for i in acc_data_dic:
            acc_data_dic[i]["Defaulting Competency"]=i
            acc_data_dic[i]["Type"]="Account"
        for i in acc_data_dic:
            acc_data_dic[i]=acc_data_dic[i][acc_data_dic[i]["Gap"]<0]
        acc_data=acc_data_dic[list(acc_data_dic)[0]]
        for i in list(acc_data_dic)[1:]:
            acc_data=pd.concat([acc_data,acc_data_dic[i]],axis=0,ignore_index=True)
        return acc_data,Names,acc_level_competencies,acc_data_dic
    def dataframe(self,ch):
        import pandas as pd
        import os
        arr=os.listdir(".")
        files=[]
        fileName=""
        for i in arr:
            if (".xlsx" in i) or (".xlsm" in i):
                files.append(i)
        for i in files:
            if ch.upper() in i.upper():
                fileName=i
        if fileName != "":
            df=pd.read_excel(fileName,sheet_name="Role- Competency Mapping",skiprows=2)
            df2=pd.read_excel(fileName,sheet_name="Role- Competency Mapping",skiprows=1)
            df=df.drop(0)
            df=df.drop("Team",axis=1)
            competencies=df2.columns.tolist()
            for i in range(len(competencies)):
                if "Unnamed:" in competencies[i]:
                    competencies[i]=""
            while "" in competencies:
                competencies.remove("")
            Names=df[df.columns[:2]]
            df=df.drop(['Emp ID', 'Name of the Resources', 'Role'],axis=1)
            arr=[]
            for i in range(3,len(df.columns.tolist())+1,3):
                arr.append(df[df.columns.tolist()[i-3:i]])
            data=[]
            for i in range(len(arr)):
                data.append(pd.concat([Names,arr[i]],axis=1))
            data_dic={}
            for i in range(len(competencies)):
                data_dic[competencies[i]]=data[i]
            for i in data_dic:
                data_dic[i]=data_dic[i].rename(columns={data_dic[i].columns.tolist()[4]: "Gap"})
                data_dic[i]=data_dic[i].rename(columns={data_dic[i].columns.tolist()[2]: "Required"})
                data_dic[i]=data_dic[i].rename(columns={data_dic[i].columns.tolist()[3]: "Current"})
            for i in data_dic:
                data_dic[i]['Date']=" "
            for i in data_dic:
                data_dic[i]=data_dic[i][data_dic[i]["Gap"]<0]
            counts=[]
            for i in data_dic:
                counts.append(data_dic[i]["Emp ID"].count())
            counts=tuple(counts)
            headings=tuple(competencies)
            return data_dic,counts,headings,competencies,Names
        else:
            return fileName,fileName,fileName,fileName,fileName
    		