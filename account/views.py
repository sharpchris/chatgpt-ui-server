import csv
import os
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
from chat.models import Setting
from allauth.account import app_settings as allauth_account_settings


class RegistrationView(RegisterView):
    def create(self, request, *args, **kwargs):
        try:
            open_registration = Setting.objects.get(name='open_registration').value == 'True'
        except Setting.DoesNotExist:
            open_registration = True

        if open_registration is False:
            return Response({'detail': 'Registration is not yet open.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check to see if the user is in the allow list
        valid_emails = get_emails_from_csv()
        if request.data['email'] not in valid_emails:
            print(f"The email address {request.data['email']} was not in the list of valid addresses")
            response = Response({'detail': f"The email address {request.data['email']} is not in the list of allowed emails. Please use your UF email account, or contact the instructor."}, status=status.HTTP_403_FORBIDDEN)
        else:
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = self.get_response_data(user)

            data['email_verification_required'] = allauth_account_settings.EMAIL_VERIFICATION

            if data:
                response = Response(
                    data,
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            else:
                response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response

def get_emails_from_csv():
    """
    Extracts a list of emails from the specified CSV file.

    Args:
    file_path (str, optional): Path to the CSV file. Defaults to "valid_emails.csv".

    Returns:
    list: A list of extracted email addresses.
    """

    # Get the script's directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine the script directory and filename to form the complete path
    file_path = os.path.join(script_dir, "jury_accounts/valid_emails.csv")

    print(f"Checking the file path: {file_path}", flush=True)

    emails = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            email = row[0] # Assuming emails are in the first column
            emails.append(email)
    
    print(f"I found {len(emails)} emails")
    return emails