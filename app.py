from flask import Flask ,render_template,request
import mysql.connector
import json


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="rest_api"
)

mycursor = mydb.cursor(buffered=True)














app = Flask(__name__)

@app.route('/api/v1/customers',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
@app.route('/api/v1/customers/',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def customers():
	api={}
	if(request.args.get('token')=='12345'):
		if request.method in ['POST','GET']:
			if request.method=='GET':
				api['method']=request.method
				api['message']="Success"
				api['customers']=[]
				mycursor.execute("SELECT * FROM customers")
				myresult = mycursor.fetchall()
				for x in myresult:
					print(x)
					api['customers'].append({'id':x[0],"name":x[1],"company_name":x[2],"phone":x[3],"address":x[4]})
				api=json.dumps(api)
				return render_template('api.html',api=api)
			else:
				api['method']=request.method
				if len(request.form)!=0:
					c=str(request.form).count('\\n')
					if(c==0):
						req=json.dumps(request.form)
						req=json.loads(req)
						
						
				if request.get_json()is not None:
					req=request.get_json()
					
					
				print(req)
				if( 'name' not in req):
					api['code']=400
					api['message']='Name is required'
					return render_template('api.html',api=api),400
				name=req['name']
				if 'company_name' in req:
					cname=req['company_name']
				else:
					cname=''
				if 'phone' in req:
					phone=req['phone']
				else:
					phone=''
				if 'address' in req:
					address=req['address']
				else:
					address=''
				sql = "INSERT INTO customers (name,company_name,phone,address) VALUES (%s, %s,%s,%s)"
				val = (name,cname,phone,address)
				print(val)
				mycursor.execute(sql, val)
				mydb.commit()
				api['message']="Success"
				api=json.dumps(api)
				return render_template('api.html',api=api),201
	else:
		api['code']=401
		api['message']='Please check your token'
		api=json.dumps(api)
		return render_template('api.html',api=api),401


@app.route('/api/v1/invoices',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
@app.route('/api/v1/invoices/',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def invoices():
	api={}
	if(request.args.get('token')=='12345'):
		if request.method in ['POST','GET']:
			if request.method=='GET':
				api['method']=request.method
				api['message']="Success"
				api['invoices']=[]
				mycursor.execute("SELECT * FROM invoices")
				myresult = mycursor.fetchall()
				for x in myresult:
					print(x)
					id=x[0]
					invoicedate=x[1]
					cuscode=x[2]
					mycursor.execute("SELECT * FROM customers where id='"+cuscode+"'")
					cusdetails=mycursor.fetchall()
					cusdetails=cusdetails[0]
					cusdetails={"name":cusdetails[1],"company_name":cusdetails[2],"phone":cusdetails[3],"address":cusdetails[4]}
					mycursor.execute("SELECT * FROM inv_item where 	invoicecode='"+str(id)+"'")
					items=[]
					noitems= mycursor.fetchall()
					for i in noitems:
						items.append({"item_name":i[1],"quantity":int(i[3]),"cost":float(i[2])})
					discount=float(x[3])
					sublotal=float(x[4])
					total=float(x[5])
					invoicedate=str(invoicedate).split('-')
					invoicedate=invoicedate[2]+'-'+invoicedate[1]+'-'+invoicedate[0]
					api['invoices'].append({"id":int(id),"invoice_date":invoicedate,"customer_details":cusdetails,"line_items":items,"subtotal":sublotal,"discount":discount,"total":total})
					
					
					
				api=json.dumps(api)
				return render_template('api.html',api=api)
			else:
				api['method']=request.method
				if len(request.form)!=0:
					c=str(request.form).count('\\n')
					if(c==0):
						req=json.dumps(request.form)
						req=json.loads(req)
						
						
				if request.get_json()is not None:
					req=request.get_json()
					
					
				print(req)
				if( 'invoice_date' not in req or 'cuscode' not in req or 'line_items' not in req  ):
					api['code']=400
					api['message']='invoice_date,cuscode,line_items are required'
					return render_template('api.html',api=api),400
				
				if 'discount' in req:
					discount=float(req['discount'])
				else:
					discount=0.0
				invoice_date=req['invoice_date']
				cuscode=req['cuscode']
				line_items=req['line_items']
				sql="select max(id) from invoices"
				mycursor.execute(sql)
				preid=mycursor.fetchall()[0][0]
				print("\n\n\ncheck 002 ",preid,"\n\n\n")
				if preid is None:
					preid=1
				else:
					print("\n\n\ncheck 002 ",preid,"\n\n\n")
					preid=int(preid)+1
				
				subtotal=0
				line_items=json.loads(line_items)
				for i in line_items:
					
					mycursor.execute("SELECT * FROM menu where id="+str(i[0]))
					
					myresult =mycursor.fetchall()[0]
					
					sql = "INSERT INTO inv_item(invoicecode,itemname,cost,quantity) VALUES (%s,%s,%s,%s)"
					val = (preid,myresult[1],myresult[2],i[1])
					subtotal+=(float(myresult[2])*i[i])
					print(myresult[2])
					mycursor.execute(sql, val)
					mydb.commit()
				sql ="INSERT INTO invoices(invoice_date,cuscode,discount,subtotal,total) VALUES (%s,%s,%s,%s,%s)"
				total=subtotal-(subtotal*discount/100)
				val=(invoice_date,cuscode,discount,subtotal,total)
				mycursor.execute(sql, val)
				mydb.commit()
				api['message']="Success"
				api=json.dumps(api)
				return render_template('api.html',api=api),201
	else:
		api['code']=401
		api['message']='Please check your token'
		api=json.dumps(api)
		return render_template('api.html',api=api),401







@app.route('/api/v1/menu',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
@app.route('/api/v1/menu/',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def menu():
	api={}
	if(request.args.get('token')=='12345'):
		if request.method in ['POST','GET']:
			if request.method=='GET':
				api['method']=request.method
				api['message']="Success"
				api['menu']=[]
				mycursor.execute("SELECT * FROM menu")
				myresult = mycursor.fetchall()
				for x in myresult:
					print(x)
					api['menu'].append({'id':x[0],"name":x[1],"cost":float(x[2])})
				api=json.dumps(api)
				return render_template('api.html',api=api)
			else:
				api['method']=request.method
				if len(request.form)!=0:
					c=str(request.form).count('\\n')
					if(c==0):
						req=json.dumps(request.form)
						req=json.loads(req)
						
						
				if request.get_json()is not None:
					req=request.get_json()
					
					
				print(req)
				if( 'name' not in req or 'cost' not in req):
					api['code']=400
					api['message']='Name and Cost is required'
					print(api)
					return render_template('api.html',api=api),400
				name=req['name']
				cost=float(req['cost'])			
				sql = "INSERT INTO menu (name,cost) VALUES (%s,%s)"
				val = (name,cost)
				print(val)
				mycursor.execute(sql, val)
				mydb.commit()
				api['message']="Success"
				api=json.dumps(api)
				return render_template('api.html',api=api),201
	else:
		api['code']=401
		api['message']='Please check your token'
		api=json.dumps(api)
		return render_template('api.html',api=api),401


@app.route('/<path:p>')
def pagenotfound(p):
	api={}
	api["code"]=404
	api["message"]="there is no such page"
	api=json.dumps(api)
	return render_template('api.html',api=api),404
@app.route('/')
def index():
	t1=[]
	t2=[]
	t3=[]
	t4=[]
	mycursor.execute("SELECT * FROM menu")
	myresult = mycursor.fetchall()
	for x in myresult:
		t1.append(x)
	mycursor.execute("SELECT * FROM customers")
	myresult = mycursor.fetchall()
	for x in myresult:
		t2.append(x)
	mycursor.execute("SELECT * FROM inv_item")
	myresult = mycursor.fetchall()
	for x in myresult:
		t3.append(x)
	mycursor.execute("SELECT * FROM invoices")
	myresult = mycursor.fetchall()
	for x in myresult:
		t4.append(x)
	return render_template('4col.html',t1=t1,t2=t2,t3=t3,t4=t4)
	
@app.route('/test/',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
@app.route('/test',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])

def test():
	if request.method in ['POST','GET','PUT','DELETE']:
		print(request.method)
		api={}
		api['type']=request.method
		api['queryParam']=request.args
		api['body']={}
		check=1
		if len(request.form)!=0:
			c=str(request.form).count('\\n')
			if(c==0):
				api['body']=request.form
				api['message']='data is in body->x-www-urlencoded'
				check=0
		if request.get_json()is not None:
			api['body']=request.get_json()
			api['message']='data is in body->raw'
			check=0
		if(check!=0):
			api['message']="do data in the body"
		
		
		api=json.dumps(api)
		return render_template('api.html',api=api)
	else:
		api={'code':501,"message":"kindly use ['POST','GET','PUT','DELETE']"}
		api=json.dumps(api)
		print(api)
		return render_template('api.html',api=api),501


@app.route('/api/v1/<string:type>/<string:id>',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
@app.route('/api/v1/<string:type>/<string:id>/',methods = ['POST', 'GET','PUT','DELETE','LINK','PATCH','COPY','HEAD','OPTIONS','UNLINK','PURGE','LOCK','UNLOCK','PROPFIND','VIEW'])
def listing(type,id):
	if(request.args.get('token')=='12345' and request.method=="GET"):
		if(type=='customers'):
			mycursor.execute("SELECT * FROM customers where id ='"+id+"'")
			myresult = mycursor.fetchall()
			if mycursor.rowcount==0:
				return render_template('api.html',api='{"code":400,"message":"unknown coustomer"}'),400
			myresult=myresult[0]
			api={}
			api['id']=myresult[0]
			d={"name":myresult[1],"company_name":myresult[2],"phone":myresult[3],"address":myresult[4]}
			api["coustomer_details"]=d
			mycursor.execute("SELECT sum(total) from invoices where cuscode ='"+id+"'")
			myresult = mycursor.fetchall()
			totalcost=myresult[0][0]
			mycursor.execute("SELECT * from invoices where cuscode ='"+id+"'")
			count=mycursor.rowcount
			api['invoice_details']={"no_of_invoices":count,"invoice_amount":totalcost}
			api=json.dumps(api)
			return render_template('api.html',api=api)
			
		elif(type=='invoices'):
			api={}
			api['method']=request.method
			api['message']="Success"
			api['invoices']=[]
			mycursor.execute("SELECT * FROM invoices where id='"+id+"'")
			if mycursor.rowcount==0:
				return render_template('api.html',api='{"code":400,"message":"unknown coustomer"}'),400
			myresult = mycursor.fetchall()
			for x in myresult:
				print(x)
				id=x[0]
				invoicedate=x[1]
				cuscode=x[2]
				mycursor.execute("SELECT * FROM customers where id='"+cuscode+"'")
				cusdetails=mycursor.fetchall()
				cusdetails=cusdetails[0]
				cusdetails={"name":cusdetails[1],"company_name":cusdetails[2],"phone":cusdetails[3],"address":cusdetails[4]}
				mycursor.execute("SELECT * FROM inv_item where 	invoicecode='"+str(id)+"'")
				items=[]
				noitems= mycursor.fetchall()
				for i in noitems:
					items.append({"item_name":i[1],"quantity":int(i[3]),"cost":float(i[2])})
				discount=float(x[3])
				sublotal=float(x[4])
				total=float(x[5])
				invoicedate=str(invoicedate).split('-')
				invoicedate=invoicedate[2]+'-'+invoicedate[1]+'-'+invoicedate[0]
				api['invoices'].append({"id":int(id),"invoice_date":invoicedate,"customer_details":cusdetails,"line_items":items,"subtotal":sublotal,"discount":discount,"total":total})
				
					
					
				api=json.dumps(api)
				return render_template('api.html',api=api)
	elif(request.method!="GET"):
		api['code']=401
		api['message']='Please check your token'
		api=json.dumps(api)
		return render_template('api.html',api=api),401
	else:
		api['code']=501
		api['message']="kindly use ['GET']"
		api=json.dumps(api)
		return render_template('api.html',api=api),501
		



app.run(debug=True)