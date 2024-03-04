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
        valid_emails = ["student8@ufl.edu","student9@ufl.edu","student10@ufl.edu"]
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
