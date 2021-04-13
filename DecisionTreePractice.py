
#Split Algorithm Class
class Record_dict(dict):
	"""docstring for node_dict"""
	def __init__(self,node_obj):
		super(Record_dict, self).__init__()
		key=node_obj.attribute
		node_obj.record_dict={}
		self[key]=node_obj.record_dict

class Split(object):
		"""docstring for Split"""
		def __init__(self,sequence):
			super(Split, self).__init__()
			self.sequence=sequence
			self.pickouter=Pickouter(sequence)
		def hunt(self,node_obj):
			#init
			tem_node=node_obj
			while self.next_att(tem_node.attribute):
				
				if tem_node.class_is_impure==False:
					tem_node.gen_leave()
					break
				if self.next_att(tem_node.attribute)=='over':
					tem_node.gen_leave()
					
					break
				#when WHILE has no signal,it will loop till no signal
				for b2c in tem_node.branches2c:
					tem_df=tem_node.data 
					new_df=tem_df[tem_df[tem_node.attribute]==b2c]
					c_node=tem_node.gen_node(
						gen_attribute=self.next_att(tem_node.attribute),gen_branch=b2c,gen_df=new_df)
					
					self.hunt(c_node)
				return None
				
		def next_att(self,current_att):

			if self.sequence.index(current_att)+1<len(self.sequence):
				return self.sequence[self.sequence.index(current_att)+1]
			else:
				
				return 'over'
				
		def gini_index(self,node):
			sum_Gini=0
			#culculate the gini_index before split
			for branch in node.branches2c:

				
				class_obj=ct(node.data['Survived'][node.data[node.attribute]==branch])
				class_all=node.data['Survived'][node.data[node.attribute]==branch]
				weight_of_branch=len(node.data[node.data[node.attribute]==branch])/len(node.data)
	
				
				gini_of_branch=weight_of_branch*(1-sum([(x[1]/len(class_all))**2 for x in class_obj.most_common()]))

				
				sum_Gini=sum_Gini+gini_of_branch
			return sum_Gini
		

		def gini_selector(self,node,branch,valid_att_list):
			#sub set
			#print('split on',node.attribute,'--',branch,'-->new_node')
			tem_data=node.data[node.data[node.attribute]==branch]
			fake_node_with_top_gini=FakeNode(attribute=valid_att_list[0],up_data=tem_data)
			for att in valid_att_list:
				fake_node=FakeNode(attribute=att,up_data=tem_data)
				#print(att,'\'s gini =',self.gini_index(fake_node))

				if self.gini_index(fake_node_with_top_gini)>self.gini_index(fake_node):
					fake_node_with_top_gini=fake_node
			return fake_node_with_top_gini
		def root_node_selector(self):
			fake_node_with_top_gini=FakeNode(attribute=self.sequence[0],up_data=g_df)
			for att in self.sequence:


				fake_node=FakeNode(attribute=att,up_data=g_df)
				#print(att,'\'s gini =',self.gini_index(fake_node))
				if self.gini_index(fake_node_with_top_gini)>self.gini_index(fake_node):
					fake_node_with_top_gini=fake_node
			return fake_node_with_top_gini
			
#*******************************************************************************************************
		def CART(self,tem_node):
			#init when node ==1
			
			
			while (self.pickouter.next_att2(tem_node)!=False) & (tem_node.class_is_impure==True):#pickouter return a list
				for b2c in tem_node.branches2c:
					#insert this node into gini_selector

					candidate=self.gini_selector(node=tem_node,branch=b2c,valid_att_list=self.pickouter.next_att2(tem_node))
					#this candidate is a fake node

					tem_df=tem_node.data 
					new_df=tem_df[tem_df[tem_node.attribute]==b2c]
					#turn fake node into real node
					c_node=tem_node.gen_node(
						gen_attribute=candidate.attribute,gen_branch=b2c,gen_df=new_df)
					
					self.CART(c_node)
				
				break
			else:
				
				tem_node.gen_leave()
				return None
#pickouter used to pick out the next 
class Pickouter(object):
	"""docstring for Pickouter"""
	def __init__(self,sequence):
		super(Pickouter, self).__init__()
		self.sequence=sequence
	def next_att2(self,node):
		tem_trace=node.trace
		valid_att_list=[]
		for att in self.sequence:
			if att not in tem_trace:
				valid_att_list.append(att)
		valid_att_list.remove(node.attribute)
		if valid_att_list!=[]:
			return valid_att_list
		else:
			return False
		

#fake nodes will be used to compute gini index
class FakeNode(object):
	"""Fake_node"""
	def __init__(self,attribute=None,up_data=None):
		super(FakeNode, self).__init__()
		self.attribute=attribute
		self.data=up_data
		self.branches2c=self.gen_branches2c()
	def gen_branches2c(self):
		tem_po_bran=list(self.data[self.attribute].unique())
		return tem_po_bran
					

class Node(object):
	"""Real_node"""
	def __init__(self,attribute=None,branch=None,df_upgrate=None,f_attribute=None):
		super(Node, self).__init__()
		#basic element
		self.children=[]
		self.leave=[]
		self.f_attribute=f_attribute
		#additional element
		self.attribute=attribute
		self.branch2f=branch
		#data element
		self.data=df_upgrate
		self.class_is_impure=self.CII()
		self.branches2c=self.gen_branches2c()
		self.dict={}
		self.trace=[]
	#using index to generate data obj
	def CII(self):
		if len(self.data['Survived'].unique())==1:
			
			return False
		else:
			
			return True
	def culculate_leave(self,branch):
		tem_data=self.data
		
		tem_data=tem_data['Survived'][tem_data[self.attribute]==branch]
		label=ct(tem_data).most_common(1)
		selected_label=str(label[0][0])
		num_obj=len(tem_data)
		return selected_label,num_obj
		
	def record_dict(self,tem_dict,tem_list):
		while tem_list[1:]:

			new_dict=tem_dict[tem_list[0]]
			return self.record_dict(new_dict,tem_list[1:])
		else:
			
			tem_dict[tem_list[-1]][self.attribute]={}
			for branch in self.branches2c:

				tem_dict[tem_list[-1]][self.attribute][str(branch)]={}
	def record_dict_leaves(self,tem_dict,tem_list):
		while tem_list[1:]:

			new_dict=tem_dict[tem_list[0]]
			return self.record_dict_leaves(new_dict,tem_list[1:])
		else:
		
			for branch in self.branches2c:
				label,numobj=self.culculate_leave(branch)

				tem_dict[tem_list[-1]][str(branch)]=str(label)#+'\n#'+str(numobj)
			
	def gen_data(self,f_data):
		#data need to be upgrate
		tem_data=g_df[g_df[self.attribute]==self.edge]
		if tem_data.empty:
			tem_data=g_df[g_df[self.attribute]==int(self.edge)] 
		#test 
		if tem_data.empty:
			print(self.attribute,'has no data obj!!!!!!!!!!!!!!!')
		return tem_data
	
	def gen_branches2c(self):
		tem_po_bran=list(self.data[self.attribute].unique())
		return tem_po_bran
	
	def gen_node(self,gen_attribute,gen_branch,gen_df):
		#generate children node
		tem_node=Node(
			attribute=gen_attribute,branch=gen_branch,df_upgrate=gen_df,f_attribute=self.attribute)
		#generate children list
		self.children.append(tem_node)
		#add trace
		tem_node.trace=self.trace+[self.attribute]+[str(gen_branch)]
		#add to node_list
		node_list.append(tem_node)
		#add to node_dict
		tem_node.record_dict(node_dict,tem_node.trace)
		return tem_node
	
	def gen_leave(self):
		#using major voting system
		tem_class=ct(self.data['Survived']).most_common(1)
		tem_class=tem_class[0][0]
		self.leave.append(tem_class)
		self.trace=self.trace+[self.attribute]

		self.record_dict_leaves(node_dict,self.trace)
	def gen_fake_node(self):
		tem_node=Node(
			attribute=gen_attribute,df_upgrate=gen_df)
		return tem_node


	

class Tree(object):
	"""docstring for Tree"""
	def __init__(self):
		super(Tree, self).__init__()
		self.test_set=[]
		self.test_mark=[]
		self.root_node=None
		self.trace=[]
		self.trace_list=[]
	def normal_hunt_tree(self):
		global node_dict
		#init root node
		self.root_node=Node(attribute='PC',df_upgrate=g_df)
		#init dict
		node_dict[self.root_node.attribute]={}
		for branch in self.root_node.branches2c:
			node_dict[self.root_node.attribute][str(branch)]={}
		print(node_dict)
		Question_1=Split(sequence=['PC','Age','Sex','SS'])
		Question_1.hunt(self.root_node)

	def CART_alg(self):
		#init root node
		Question_2=Split(sequence=['PC','Age','Sex','SS'])
		fake_root_node=Question_2.root_node_selector()
		
		root_node=Node(attribute=fake_root_node.attribute,df_upgrate=g_df)
		self.root_node=root_node
		node_list.append(self.root_node)

		#add to node dict
		node_dict[self.root_node.attribute]={}
		for branch in self.root_node.branches2c:
			node_dict[self.root_node.attribute][str(branch)]={}
		#compute precedure
		
		Question_2.CART(root_node)
	def plot_tree(self):
		#plot the tree
		Plot.createPlot(node_dict)
		#image the testset
	def load_test_set(self,test_set):
		
		for i in range(len(test_set.index)):
			a=test_set.iloc[i,:]
			b=a.to_dict()
			self.test_set.append(b)
			self.test_mark.append(a['Survived'])
		return self.test_set 


	def insert(self,tem_dict):
		while type(tem_dict)==dict_type:
			try:
				tem_keys=tuple(tem_dict.keys())[0]
				edge_key=str(self.tem_test_set_line[tem_keys])
				new_dict=tem_dict[tem_keys][edge_key]
				
				return self.insert(new_dict)
			except KeyError as e:
				#print('One node called %s lost'%(edge_key))
				return 'No result'
			
		else:

			return tem_dict
		

	def insert_associate(self,tem_dict):
		#turn into trace style
		while type(tem_dict)==dict_type:
			try:
				tem_keys=tuple(tem_dict.keys())[0]
				edge_key=str(self.tem_test_set_line[tem_keys])
				new_dict=tem_dict[tem_keys][edge_key]
				self.trace.append(tem_keys)
				self.trace.append(edge_key)
				return self.insert_associate(new_dict)
			except KeyError as e:
				#print('One node called %s lost'%(edge_key))
				return 'No result'
			
		else:
			self.trace.append(tem_dict)

			return tem_dict
	def list_to_str(self,list_obj):
		b=[str(x)+'->' for x in list_obj]

		b=str(b)
		b=b.replace(',','')
		
		b=b.replace('\'','')
		return b
	def apply(self):
		global result_df 
		for tem_data in self.test_set:
			self.tem_test_set_line=tem_data
			result=self.insert(node_dict)
			#tem_data['Result']=result
			#result_df=result_df.append(tem_data,ignore_index=True)
		#print('size of processed data is',len(self.test_set))
		#init self.test_set
		self.test_set=[]
			
	def apply_associate(self):
		global result_df 
		for tem_data in self.test_set:
			self.tem_test_set_line=tem_data
			result=self.insert_associate(node_dict)
			tem_data['Result']=result
			result_df=result_df.append(tem_data,ignore_index=True)
			self.trace=self.list_to_str(self.trace)

			self.trace_list.append(self.trace)
			#print(self.trace)
			self.trace=[]

	def associate(self):
		associate_dict=ct(self.trace_list)
		return associate_dict

	def regular(self,node_dict):
		
		d=node_dict
		d['PC']['1']['Age']['child']='0'
		d['PC']['3']['Age']['child']['Sex']['female']='0'
class DataDownload(object):
	"""docstring for DataDownload"""
	def __init__(self):
		super(DataDownload, self).__init__()
	def series_to_csv(self,data_dict,name_str):
		tem_series=pd.Series(data_dict)
		tem_series.to_csv('/Users/dawson/Scripts/CSV_FILE/'+name_str+'.csv')
		print('data has been down load')
		
			
class Purner(object):
	"""docstring for Purner"""
	def __init__(self):
		super(Purner).__init__()

	def post_purning(self,dict_obj):
		tem_dict=dict_obj
		tem_dict['PC']['3']['Age']['adult']['Sex']['male']='0'
		tem_dict['PC']['3']['Age']['child']['Sex']['male']='0'
		tem_dict['PC']['3']['Age']['child']['Sex']['female']='1'
		tem_dict['PC']['3']['Age']['teenage']['Sex']['male']='0'
		tem_dict['PC']['1']['Age']['adult']['Sex']['female']='1'
		tem_dict['PC']['1']['Age'].pop('teenage')
		tem_dict['PC']['2']['Age']['teenage']['Sex']['female']='1'
		tem_dict['PC']['2']['Age']['teenage']['Sex']['male']='0'
		tem_dict['PC']['2']['Age']['adult']['Sex']['female']='1'
		tem_dict['PC']['2']['Age']['adult']['Sex']['male']='0'
		tem_dict['PC']['2']['Age']['child']='1'
		tem_dict['PC']['1']['Age']['adult']['Sex']['male']='0'
	def post_purning_for_CART(self,tem_dict):
		tem_dict['Sex']['male']['Age']['adult']='0'
		tem_dict['Sex']['male']['Age']['child']['PC']['3']['SS'].pop('0')
		tem_dict['Sex']['male']['Age']['child']['PC']['2']='1'
		tem_dict['Sex']['male']['Age']['teenage']='0'
		tem_dict['Sex']['female']['PC']['1']='1'
		tem_dict['Sex']['female']['PC']['3']['SS']['0']='1'
		tem_dict['Sex']['female']['PC']['2']='1'
		



						

		
			



		
		
if __name__ == '__main__':
		from pprint import pprint
		import pandas as pd 
		from collections import Counter as ct
		import TreePlot_test as Plot
		import time
		#init global variables
		global g_df,node_list,node_dict,dict_type,result_df
		new_purner=Purner()
		g_df=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/trainDataset.csv')
		add_g_df=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/trainDataset.csv')
		node_list=[]
		node_dict={}
		dict_type=type(node_dict)
		result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		downloader=DataDownload()
		
		#ID3
		
		RTR_df=pd.DataFrame()
		new_tree=Tree()
		new_tree.normal_hunt_tree()
			#regulate
		new_tree.regular(node_dict)
		
		#new_tree.plot_tree()
		
		testset=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/testDataset.csv')
		
		new_tree.load_test_set(testset)
		RTR=[]
		for i in range(17):
			start=time.clock()
			new_tree.apply()
			end=time.clock()
			RTR.append(end-start)
			testset=testset.append(testset)
			new_tree.load_test_set(testset)
			print(i)
		tme_s=pd.Series(RTR)
		RTR_df.insert(RTR_df.shape[1],'Hunt',tme_s)
		
		
		#new_tree.plot_tree()
		'''
		print('this table is ID3')


		print(result_df)
		accurate=0
		for i in range(len(result_df)):
			if str(result_df.iloc[i,0])==str(result_df.iloc[i,5]):
				accurate+=1
		accurate=round(accurate/len(result_df)*100,2)
		print('The accurate persentage is:',accurate,'%')
		result_df.to_csv('/Users/dawson/Scripts/CSV_FILE/Result_hunt_trainset.csv')
		#post-purning

		#init the result table
		#result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		
		'''
		result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		node_dict={}
		node_list=[]
		third_tree=Tree()
		third_tree.normal_hunt_tree()
			#regulate
		third_tree.regular(node_dict)
		testset=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/testDataset.csv')
		third_tree.load_test_set(testset)
		new_purner.post_purning(node_dict)
		RTR=[]
		for i in range(17):
			start=time.clock()
			third_tree.apply()
			end=time.clock()
			RTR.append(end-start)
			testset=testset.append(testset)
			third_tree.load_test_set(testset)
			print(i)
		tme_s=pd.Series(RTR)
		RTR_df.insert(RTR_df.shape[1],'Pruned Hunt',tme_s)
		#new_tree.plot_tree()
		#print('this table is ID3 after post-purning')
		#print(result_df)
		
		'''
		accurate=0
		for i in range(len(result_df)):
			if str(result_df.iloc[i,0])==str(result_df.iloc[i,5]):
				accurate+=1
		accurate=round(accurate/len(result_df)*100,2)
		
		#print('The accurate persentage is:',accurate,'%')

		#download to csv
		#result_df.to_csv('/Users/dawson/Scripts/CSV_FILE/Result_hunt_after_purning.csv')
		#compute s and c
	
		a_data=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/trainDataset.csv')
		new_tree.load_test_set(a_data)
		new_tree.apply_associate()

		ass_CART_result=new_tree.associate()
		downloader.series_to_csv(data_dict=ass_CART_result,name_str='Association_Hunt_data')
		
		
		
		#CART AlG
		
		RunTime=[]
		for i in range(20):
			second_tree=Tree()
			start=time.clock()

			second_tree.CART_alg()
			end = time.clock()
			print('The (',i,'/1000 times test, running time is:',end-start)
			RunTime.append(end-start)
			tme_s=pd.Series(RunTime)
			tme_s.to_csv('/Users/dawson/Scripts/CSV_FILE/Result_CART_Runtime.csv')
			g_df=g_df.append(g_df)
		'''
		
		
		
		node_list=[]
		node_dict={}
		
		result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		



		
		second_tree=Tree()
		second_tree.CART_alg()
		
		#new_purner.post_purning_for_CART(node_dict)

		#second_tree.plot_tree()
		
		testset=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/testDataset.csv')
		second_tree.load_test_set(testset)
		
		RTR=[]
		for i in range(17):
			start=time.clock()
			second_tree.apply()
			end=time.clock()
			RTR.append(end-start)
			testset=testset.append(testset)
			second_tree.load_test_set(testset)
			print(i)
		tme_s=pd.Series(RTR)
		RTR_df.insert(RTR_df.shape[1],'CART',tme_s)
		
		#second_tree.apply()
		
		#print('this table is CART')
		#print(result_df)
		'''
		accurate=0
		for i in range(len(result_df)):
			if str(result_df.iloc[i,0])==str(result_df.iloc[i,5]):
				accurate+=1
		accurate=round(accurate/len(result_df)*100,2)
		#print('The accurate persentage is:',accurate,'%')
		#second_tree.plot_tree()
		#post-purning
		#init result table
		result_df.drop(index=result_df.index)
		result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		second_tree.load_test_set(test_set)
		second_tree.apply()
		'''
		result_df=pd.DataFrame(columns=['Survived','PC','Sex','Age','SS','Result'])
		node_dict={}
		node_list=[]
		fourth=Tree()
		fourth.CART_alg()
			#regulate
		
		testset=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/testDataset.csv')
		fourth.load_test_set(testset)
		new_purner.post_purning_for_CART(node_dict)

		RTR=[]
		for i in range(17):
			start=time.clock()
			fourth.apply()
			end=time.clock()
			RTR.append(end-start)
			testset=testset.append(testset)
			fourth.load_test_set(testset)
			print(i)
		tme_s=pd.Series(RTR)
		#tme_s.to_csv('/Users/dawson/Scripts/CSV_FILE/Result_CART_Runtime_apply_pruned.csv')
		RTR_df.insert(RTR_df.shape[1],'pruned CART',tme_s)
		RTR_df.to_csv('/Users/dawson/Scripts/CSV_FILE/apply_time.csv')
		#second_tree.apply()
		#print('this table is CART after purning')
		#print(result_df)
		'''
		accurate=0
		for i in range(len(result_df)):
			if str(result_df.iloc[i,0])==str(result_df.iloc[i,5]):
				accurate+=1
		accurate=round(accurate/len(result_df)*100,2)
		#print('The accurate persentage is:',accurate,'%')

		#second_tree.plot_tree()
		result_df.to_csv('/Users/dawson/Scripts/CSV_FILE/Result_CART.csv')
		#compute s and c
		a_data=pd.read_csv('/Users/dawson/Scripts/CSV_FILE/trainDataset.csv')
		second_tree.load_test_set(a_data)
		second_tree.apply_associate()

		ass_CART_result=second_tree.associate()
		downloader.series_to_csv(data_dict=ass_CART_result,name_str='Association_CART_data')
		'''

		



		
		



				