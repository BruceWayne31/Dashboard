class methods():
	def dataframe(self):
		import pandas as pd
		df=pd.read_excel("F:\\VF_TWINX_Competency_Tracker.xlsx",sheet_name="Role- Competency Mapping",skiprows=2)
		df2=pd.read_excel("F:\\VF_TWINX_Competency_Tracker.xlsx",sheet_name="Role- Competency Mapping",skiprows=1)
		df=df.drop(0)
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


