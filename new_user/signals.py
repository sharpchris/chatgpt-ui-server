from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chat.models import Conversation, Message
from .jurors import instruction_prompt, jurors

@receiver(post_save, sender=User)
def test_message(sender, instance, created, **kwargs):
    if created:
        print(f"sender: {sender}")
        print(f"instance: {instance}")

        # Create all the jury members for the new user
        for juror in jurors:
            juror_convo = Conversation.objects.create(
                user = instance,
                topic = juror['name']
            )

            messages_string = f"""[{{'role': 'system', 'content': 'You are a potential juror answering questions.'}}, {{'role': 'user', 'content': "{instruction_prompt} {juror['prompt_to_describe']}"}}]"""

            # Instruction message and prompt for personality
            Message.objects.create(
                conversation = juror_convo,
                user = instance,
                message = instruction_prompt + " " + juror['prompt_to_describe'],
                messages = messages_string,
                is_hidden_from_user = True,
            )

            # A visible mssage that will be seen by the user
            Message.objects.create(
                conversation = juror_convo,
                user = instance,
                message = f"My name is {juror['name']}",
                messages = "",
                is_bot = True,
            )

