from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Quote, EmailSettings
import logging

logger = logging.getLogger(__name__)


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


@require_POST
def submit_quote(request):
    """
    Handles quote/inquiry form submissions from both the main form and popup.
    Saves to DB and emails the owner if email notifications are enabled.
    """
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    project_type = request.POST.get('project_type', '').strip()
    message = request.POST.get('message', '').strip()
    source = request.POST.get('source', 'form').strip()

    if not name or not phone:
        return JsonResponse({'success': False, 'error': 'Name and phone are required.'}, status=400)

    # Save to database
    quote = Quote.objects.create(
        name=name,
        phone=phone,
        email=email or None,
        project_type=project_type,
        message=message,
        source=source,
    )

    # Send email notification
    try:
        email_cfg = EmailSettings.get_settings()
        if email_cfg.send_email_on_inquiry and email_cfg.owner_email:
            subject = f"{email_cfg.email_subject_prefix} – {name}"
            body = f"""
New inquiry received on SUTPLY website!

━━━━━━━━━━━━━━━━━━━━━━━━
Customer Details
━━━━━━━━━━━━━━━━━━━━━━━━
Name         : {name}
Phone        : {phone}
Email        : {email or 'Not provided'}
Project Type : {project_type or 'Not specified'}
Source       : {source}

Message:
{message or '(No message provided)'}

━━━━━━━━━━━━━━━━━━━━━━━━
Received at: {quote.created_at.strftime('%d %b %Y, %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━━━━━

View all inquiries in admin: https://your-domain.com/admin/main/quote/
"""
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_cfg.owner_email],
                fail_silently=False,
            )
    except Exception as e:
        # Don't break the user experience if email fails
        logger.error(f"Failed to send inquiry email: {e}")

    return JsonResponse({'success': True, 'message': 'Inquiry submitted successfully!'})