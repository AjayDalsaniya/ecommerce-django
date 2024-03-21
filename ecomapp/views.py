
import django.conf
import django.db
from django.shortcuts import redirect, render
from django.http import response, request, HttpResponse
#from myproject.settings import AUTH_PASSWORD_VALIDATORS
from ecom.settings import STATIC_URL, TEMPLATES
from .models import *
from fpdf import FPDF
from django.template.loader import  get_template
from xhtml2pdf import pisa
import os
from io import BytesIO
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.views import View
from .models import order  # Import your Order model here
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Create your views here.

def admin_index(request):
     cid  = customer.objects.all()
     context = {
          'cid':cid,
     }
     return render(request,'ecomapp/admin/admin-panel.html',context)

def add_product(request):
     return render(request,'ecomapp/admin/add_product.html')

def product_data(request):
     try:
          if request.POST:
               mobile_name = request.POST['mobile_name']
               ram = request.POST['ram']
               rom = request.POST['rom']
               info = request.POST['info']
               price = request.POST['price']
               pic  = request.FILES['pic']

               pid = product.objects.create(
                    mobile_name = mobile_name,
                    ram = ram,
                    rom = rom,
                    info = info,
                    price = price,
                    pic = pic,


               )

               pid.save()
               context = {
               "s_msg":" product successfull"
               }
               return render(request,'ecomapp/admin/add_product.html',context)
          else:
               context = {
               "s_msg":"product faild "
               }
               return render(request,'ecomapp/admin/add_product.html',context)
          
     except:
          context = {
               "s_msg":"Data Fillup "
               }
          return render(request,'ecomapp/admin/add_product.html',context)


     
def all_product(request):
     pall = product.objects.all()
     context = {
          "pall":pall,
     }
     return render(request,'ecomapp/admin/all_product.html',context)


def view_product(request,pk):
     pid = product.objects.get(id = pk)
     context = {
          'pid':pid,
     }
     return render(request,'ecomapp/admin/view_product.html',context)


def edit_product(request,pk):
     pid = product.objects.get(id = pk)
     context = {
          'pid':pid,
     }
     return render(request,'ecomapp/admin/edit_product.html',context)

def update_product(request):
     if request.POST:
          id = request.POST['id']
          mobile_name = request.POST['mobile_name']
          ram = request.POST['ram']
          rom = request.POST['rom']
          info = request.POST['info']
          price = request.POST['price']
          #pic = request.FILES['pic']

          pid = product.objects.get(id = int(id))
          pid.mobile_name = mobile_name
          pid.ram = ram
          pid.rom = rom
          pid.info = info
          pid.price = price
          if 'pic' in request.FILES:
               pid.pic = request.FILES['pic']

          pid.save()
          context = {
          'pid':pid,
          "s_msg":"product update "
          }
          return render(request,'ecomapp/admin/edit_product.html',context)
     else:
          context = {
          'pid':pid,
          "s_msg":"not updated "
          }
          return render(request,'ecomapp/admin/edit_product.html',context)

def delete_product(request,pk):
     pid = product.objects.get(id = pk)
     pid.delete()
     pid = product.objects.all()
     
     return redirect('all-product')



def all_order(request):
     oid = order.objects.all()
     context = {
          'oid':oid,
     }
     return render(request,'ecomapp/admin/all-order.html',context)

def view_order1(request,pk):
     oid = order.objects.get(id = pk)
     context = {
               'oid':oid,
          }
     return render(request,'ecomapp/admin/view_order.html',context)
    

def status(request):
     try:
          if request.POST:
               id = request.POST['id']
               st1 = request.POST['status']
               status = 0
               if st1 == "Pending":
                    status = 0
               else:
                    status = 1
               print("status.................. : ",status)

               oid  = order.objects.get(id = id)
               oid.status = status
               oid.save()
               oid = order.objects.all()
               context = {
                    'oid':oid,
               }
               return render(request,'ecomapp/admin/all-order.html',context)
     except Exception as e:
          print("......................... e ",e)





#----------customer - panel-----------------------------------------------------------------------------------------------------------------


def customer_index(request):
     if "email" in request.session:
        uid = user.objects.get(email = request.session["email"])
        cid  = customer .objects.get(cust_id = uid)
        if uid.role == "customer":
          pid = product.objects.all()
          context = {
               'cid':cid,
               'pid':pid,
          }
          return render(request,'ecomapp/customer/customer_index.html',context)
     else:
          pid = product.objects.all()
          context = {
              
               'pid':pid,
          }
          return render(request,'ecomapp/customer/customer_index.html',context)

def view_product_cust(request,pk):
     if "email" in request.session:
          uid = user.objects.get(email = request.session['email'])
          cid = customer.objects.get(cust_id = uid)
          pid = product.objects.get(id = pk)
          context = {
               'pid':pid,
               'uid':uid,
               'cid':cid,
          }
          return render(request,'ecomapp/customer/view_product_cust.html',context)

def buynow(request,pk):
    if "email" in request.session:
          uid = user.objects.get(email = request.session['email'])
          cid = customer.objects.get(cust_id = uid)

          pid  = product.objects.get(id = pk)
          context = {
          'pid':pid,
          'uid':uid,
          'cid':cid,
          }
          return render(request,'ecomapp/customer/order.html',context)
    else:
         return render(request,'ecomapp/auth/login.html')
    

# Add to cart 
def addToCart(request):
     return render(request,"ecomapp/customer/addtocart.html")



from django.core.mail import EmailMultiAlternatives

def order_product(request):
     if "email" in request.session:
          uid = user.objects.get(email = request.session['email'])
          cid = customer.objects.get(cust_id = uid)

          try:
               
               if request.POST:



                    pid  = request.POST['id']
                    name  = request.POST['name']
                    mobile_no  = request.POST['mobile_no']
                    country  = request.POST['country']
                    state  = request.POST['state']
                    city  = request.POST['city']

                    productname  = request.POST['productname']
                    ram  = request.POST['ram']
                    rom  = request.POST['rom']
                    price  = int(request.POST['price'])
                    qty  = int(request.POST['qty'])
                    
                    total_price = price *qty

                    pid = product.objects.get(id = pid)

                    oid = order.objects.create(
                         product_id = pid,
                         user_id = uid,
                         cust_id = cid,
                         name = name,
                         mobile_no = mobile_no,
                         country = country,
                         state = state,
                         city = city,
                         productname = productname,
                         ram = ram,
                         rom = rom,
                         price = price,
                         qty = qty,
                         total_price = total_price

                    )
                    oid.save()

                    context = {
                         'oid':oid,
                         'uid':uid,
                         'cid':cid,
                         "s_msg":" order successfull"

                    }
                    #----------------------------------------------------------------------------------------------
                   
                    try:
                         oid = order.objects.get(id= oid.id)  # you can filter using order_id as well
                    except order.DoesNotExist:
                         return HttpResponse("505 Not Found")
                    data = {
                         "order_id": oid.id,
                         "oid": oid
                         }

                    print("Email===================== ",oid.user_id.email)
                    email = oid.user_id.email
                    pdf = render_to_pdf('ecomapp/Invoice.html', data)


                    if pdf:
            

                         response = HttpResponse(pdf, content_type='application/pdf')
                         filename = "Invoice_%s.pdf" % (data['order_id'])
                         content = "inline; filename='%s'" % (filename)
                         # download = request.GET.get("download")
                         # if download:
                         content = "attachment; filename=%s" % (filename)
            
               
                         response['Content-Disposition'] = content
                         with open(os.path.join(settings.MEDIA_ROOT, "pdf\\"+ filename), 'wb') as f:
                              fpdf = f.write(pdf)

             



                         sender_email = "abpatel0421@gmail.com"
                         list1=email.split()
                         rec_email = list1
                         f1  = "pdf\\"+ "Invoice_%s.pdf" % (data['order_id'])
                         #password = input(str("please enter your password : "))
                         password =str("iavr livu soti qslo")
               
                         subject = "new email from tie attachment"  

                         def send_emails(rec_email):
                              for person in rec_email:

                                   body = """
                                             Certificate for COVID-19 Vaccination
                                             
                                             """
                                   msg = MIMEMultipart()
                                   msg['from'] = sender_email
                                   msg['to'] =person
                                   msg['subject'] = subject

                                   
                                   msg.attach(MIMEText(body,'plain'))


                                   filename = f1
                                   
                                   attachment = open(filename,'rb')
                                   attachment_package = MIMEBase('application','octet-stream')
                                   attachment_package.set_payload((attachment).read())
                                   encoders.encode_base64(attachment_package)
                                   attachment_package.add_header('Content-Disposition','attachment', filename=filename)
                                   msg.attach(attachment_package)
                                   
                                   text =msg.as_string()
                                   
                                   server = smtplib.SMTP('smtp.gmail.com',587)
                                   server.ehlo()
                                   server.starttls()
                                   server.login(sender_email,password)
                                   print("login success ")

                                   print(f"sending email to :{person}...")           
                                   server.sendmail(sender_email,person,text)
                                   print("email has been send to {person}")
                                   print()
                                   server.quit()

                         send_emails(rec_email)



                    return response
               #return HttpResponse("Not found")

                    return render(request,'ecomapp/customer/order.html',context)
               
               else:
                    context = {
                         
                         "s_msg":" order not successfull"

                    }
                    return render(request,'ecomapp/customer/order.html',context)
          except Exception as e :
               context = {
                         
                         'uid':uid,
                         'cid':cid,
                         "s_msg":" Data Fillup"

               }
               return render(request,'ecomapp/customer/order.html',context)
          

def view_order(request):
     if "email" in request.session:
          uid = user.objects.get(email = request.session['email'])
          cid = customer.objects.get(cust_id = uid)


          

          oid = order.objects.filter(cust_id = cid)

          for i in oid:
               print("product name---------------------------- : ",i.productname)

          context = {
               'uid':uid,
               'cid':cid,
               'oid':oid,
          }
          return render(request,'ecomapp/customer/view-order.html',context)
     else:
          context = {
               "s_msg":"no Order ",
          }
          return render(request,'ecomapp/customer/customer_index.html',context)
     


          
def logout(request):
     if "email" in request.session:
          del request.session['email']
          return render(request,'ecomapp/auth/login.html')
     else:
          return render(request,'ecomapp/auth/login.html')

def login(request):
     return render(request,'ecomapp/auth/login.html')

def login_data(request):
     if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])
        cid = customer.objects.get(cust_id = uid)

        context = {
             'uid':uid,
             'cid':cid
               }
        return render(request,'ecomapp/customer/customer_index.html',context)
     else:
          try:
               if request.POST:
                    email = request.POST['email']
                    password = request.POST['password']
                    
                    
                    uid = user.objects.get(email = email)

                    if uid.email == email and uid.password == password:
                         if uid.role == "customer":
                              request.session['email']=email
                              context = {
                                   "uid":uid,
                              }
                              return redirect('customer_index')
                              #return render(request,'ecomapp/customer/customer_index.html',context)
                         
                         elif uid.role == "admin":
                              return render(request,'ecomapp/admin/admin-panel.html')
                    else:
                         msg = "Inavlid Email and Password"
                         context = {
                              'msg':msg,
                              }
                         return render(request,'ecomapp/auth/login.html',context)
          except:
               msg = "Data Fillup!"
               context = {
                              'msg':msg,
                              }
               return render(request,'ecomapp/auth/login.html',context)


def register(request):
     return render(request,'ecomapp/auth/register.html')
     
def register_data(request):
     try:
          if request.POST:
               email = request.POST['email']
               password = request.POST['password']
               name = request.POST['name']
               country = request.POST['country']
               state = request.POST['state']
               city = request.POST['city']
               pic = request.FILES['pic']
             

               uid  = user.objects.create(
                    email = email,
                    password = password,
                    role = "customer",
                    
                    

               )
               uid.save()

               cid  = customer.objects.create(
                    cust_id = uid,
                    name = name,
                    country = country,
                    state = state,
                    city = city,
                    pic = pic,
                   
               )
               cid.save()

               return render(request,"ecomapp/auth/login.html")
          else:
               print("invalid register")

     except Exception as e:
          msg = "Data Fillup!"
          context = {
                              'msg':msg,
                              }
          return render(request,'ecomapp/auth/register.html',context)


#pdf
     



def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

class GenerateInvoice(View):
     def get(self, request, pk, *args, **kwargs):
          try:
               oid = order.objects.get(id=pk)  # you can filter using order_id as well
          except order.DoesNotExist:
               return HttpResponse("505 Not Found")
          data = {
            "order_id": oid.id,
            "oid": oid
          }

          print("Email===================== ",oid.user_id.email)
          email = oid.user_id.email
          pdf = render_to_pdf('ecomapp/Invoice.html', data)
          # return HttpResponse(pdf, content_type='application/pdf')

          # force download
          if pdf:
            

               response = HttpResponse(pdf, content_type='application/pdf')
               filename = "Invoice_%s.pdf" % (data['order_id'])
               content = "inline; filename='%s'" % (filename)
               # download = request.GET.get("download")
               # if download:
               content = "attachment; filename=%s" % (filename)
            
               
               response['Content-Disposition'] = content
               with open(os.path.join(settings.MEDIA_ROOT, "pdf\\"+ filename), 'wb') as f:
                    fpdf = f.write(pdf)

             



               