from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Gift
from .forms import GiftForm
import io
from django.http import FileResponse

# Account creation imports
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# imports and vars for reports
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.rl_config import  defaultPageSize
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
PAGE_HEIGHT= letter
PAGE_WIDTH= letter
styles = getSampleStyleSheet()


def index(request):
    gift_list = Gift.objects.order_by('id')

    form = GiftForm()

    context = {'gift_list' : gift_list, 'form' : form}

    return render(request, 'giftme/index.html', context)

def signupView(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log the user in
            login(request, user=user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'giftme/signup.html', {'form':form})

def loginView(request):
    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log the user in

            user = form.get_user()
            login(request, user=user)

            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'giftme/login.html', {'form':form})

def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('login')



@require_POST
def addGift(request):
    form = GiftForm(request.POST)

    if form.is_valid():
        new_gift = Gift(text=request.POST['text'])
        new_gift.save()

    return redirect('index')

def purchaseGift(request, gift_id):
    gift = Gift.objects.get(pk=gift_id)
    gift.purchase = True
    gift.save()

    return redirect('index')

def unpurchaseGift(request, gift_id):
    gift = Gift.objects.get(pk=gift_id)
    gift.purchase = False
    gift.save()

    return redirect('index')

def deleteGift(request,gift_id):
    gift = Gift.objects.get(pk=gift_id)
    gift.delete()
    return redirect('index')

def deleteCompleted(request):
    Gift.objects.filter(purchase__exact=True).delete()

    return redirect('index')

def deleteAll(request):
    Gift.objects.all().delete()

    return redirect('index')

def generateReport(request):

    # formatting variables , through trial and error
    LINE_SPACING = 20
    TITLE_SPACING = 40

    #Create list of gifts for report
    gift_list = Gift.objects.order_by('id')
    purchased_gift_report_list = []
    gift_report_list = []

    for gift in gift_list:
        if gift.purchase :
            purchased_gift_report_list.append(gift.text)
        else:
            gift_report_list.append(gift.text)

    pdf_generic_name = 'Wedding Gift List'

    # Create a file-like buffer to receive PDF data.
    gift_list_buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    # give A4 as standard size.
    report_page = canvas.Canvas(gift_list_buffer, pagesize=letter, pageCompression=1)

    # create report format
    title_report = pdf_generic_name
    final_text =  title_report + 'Hello World'


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    report_page.translate(inch,inch)

    # Title for the report with green font
    report_page.setFont("Helvetica", 18)
    report_page.setFillColorRGB(0.2,0.5,0.3)
    report_page.drawString(180,600, title_report)
    report_page.line(inch,590,400,590)

    # secondary Title for the purchased list
    report_page.setFont("Helvetica", 14)
    report_page.setFillColor(aColor='black')
    report_page.drawString(180, (590-(TITLE_SPACING*1)), text='Purchased Gifts:')

    # Purchased gifts
    report_page.setFont("Helvetica", 10)

    for count in range(len(purchased_gift_report_list)):
        report_page.drawString(180, (530 - (LINE_SPACING * count)), text=purchased_gift_report_list[count])

    # unPurchased gifts
    report_page.setFont("Helvetica", 14)
    new_title_start_point = (530 -(len(purchased_gift_report_list)*LINE_SPACING) -(TITLE_SPACING * 1))
    report_page.drawString(180, new_title_start_point , text='Unpurchased Gifts:')

    report_page.setFont("Helvetica", 10)
    for count in range(1,len(gift_report_list)):
        report_page.drawString(180, (new_title_start_point - (LINE_SPACING * count)), text=gift_report_list[count])

    # Close the PDF object cleanly, and we're done.
    report_page.showPage()
    report_page.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    gift_list_buffer.seek(0)
    return FileResponse(gift_list_buffer, as_attachment=True, filename= pdf_generic_name + '.pdf')


