# 📱 SMS Notification Setup Guide

## Quick Setup (5 minutes)

### Step 1: Install Twilio Package
```bash
pip install twilio
```

### Step 2: Create Twilio Account
1. Go to [Twilio.com](https://www.twilio.com)
2. Sign up for a free trial account (Free $20 credit)
3. Verify your phone number
4. Get your credentials:
   - **Account SID**: Find in Dashboard
   - **Auth Token**: Find in Dashboard  
   - **Phone Number**: Buy a Twilio number (free with trial credit)

### Step 3: Set Environment Variables

**Windows PowerShell:**
```powershell
$env:TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN="your_auth_token_here"
$env:TWILIO_PHONE_NUMBER="+1234567890"
```

**Windows Command Prompt:**
```cmd
set TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
set TWILIO_AUTH_TOKEN=your_auth_token_here
set TWILIO_PHONE_NUMBER=+1234567890
```

**Linux/Mac Bash:**
```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_PHONE_NUMBER="+1234567890"
```

### Step 4: Restart Streamlit
```bash
streamlit run app.py
```

## Verification

✅ Check if SMS is enabled:
1. Go to Owner Dashboard → Operations tab
2. Look for "✅ SMS ENABLED" message
3. View notification history at bottom

## How It Works

When an order is marked as "Ready":
1. **SMS is sent** to customer phone via Twilio
2. **Push notification** sent via ntfy.sh (backup)
3. **Log entry** created in notification history

## SMS Message Format

```
🧺 Smart Laundry: Your order #123 is READY for Delivery!
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SMS not configured" | Check environment variables are set |
| SMS not sending | Verify Twilio credentials are correct |
| Import error | Run `pip install twilio` |
| Wrong phone number | Ensure format is +COUNTRYCODE PHONENUMBER |
| Twilio shows 0 balance | Use trial account or add payment method |

## Pricing

- **Free Trial**: $20 free credit (covers ~100 SMS in India)
- **After Trial**: ~₹4-5 per SMS in India
- **No setup fees**: Just pay per message

## Environment Variable File (Optional)

Create `.env` in your project root:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

Then load it in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Support

- Twilio Docs: https://www.twilio.com/docs/sms
- Get Help: https://www.twilio.com/console/support

---

**Note**: SMS costs money. Free trial has $20 credit. Plan accordingly!
