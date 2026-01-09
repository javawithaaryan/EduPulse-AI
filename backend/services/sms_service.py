from config import Config

class SMSService:
    @staticmethod
    def send_alert(phone_number, student_name, risk_level):
        """
        Sends an SMS alert to parents.
        """
        message = f"EduPulse Alert: Your child {student_name} is at {risk_level} academic risk. Please check the dashboard."
        
        if Config.USE_MOCK_AI:
            print(f" >>> [MOCK SMS] To: {phone_number} | Msg: {message}")
            return True
        
        # Real Azure Communication Services Code
        # poller = sms_client.send(...)
        return True
