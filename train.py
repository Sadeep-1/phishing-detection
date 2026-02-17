# generate_training_data.py - Create Balanced Dataset with Nepali + English
import pandas as pd
import os

print("="*80)
print("GENERATING BALANCED TRAINING DATASET (NEPALI + ENGLISH)")
print("="*80)

# 1. Load your phishing emails
PHISHING_DATA_PATH = "data/elderly_phishing_dataset.csv"

if os.path.exists(PHISHING_DATA_PATH):
    print(f"\n✅ Loading existing phishing emails from: {PHISHING_DATA_PATH}")
    phishing_df = pd.read_csv(PHISHING_DATA_PATH)
    print(f"   Found {len(phishing_df)} phishing emails")
    
    # Find the email text column
    text_col = None
    for col in phishing_df.columns:
        if phishing_df[col].dtype == 'object':
            avg_len = phishing_df[col].astype(str).str.len().mean()
            if avg_len > 100:
                text_col = col
                break
    
    if not text_col:
        print("\n⚠️  Cannot auto-detect email text column")
        print("Available columns:")
        for i, col in enumerate(phishing_df.columns):
            print(f"  {i}: {col}")
        text_idx = int(input("Enter index of email text column: "))
        text_col = phishing_df.columns[text_idx]
    
    print(f"   Using text column: '{text_col}'")
    
    # Extract just the email text
    phishing_emails = phishing_df[text_col].astype(str).tolist()
    num_phishing = len(phishing_emails)
else:
    print(f"\n⚠️  No existing data found.")
    exit(1)

print(f"\n✅ Total phishing emails: {num_phishing}")

# 2. Generate legitimate emails (ENGLISH + NEPALI)
print("\n" + "="*80)
print("GENERATING LEGITIMATE EMAIL EXAMPLES")
print("="*80)

# Create realistic legitimate emails in BOTH languages
legitimate_emails = [
    # ===== ENGLISH LEGITIMATE EMAILS =====
    
    # Work/Business
    """Subject: Weekly Team Meeting - Thursday 3PM

Hi Team,

Just a reminder about our weekly team meeting this Thursday at 3:00 PM in Conference Room B.

Agenda:
- Project status updates
- Q&A session
- Next week's priorities

Please come prepared with your updates.

Best regards,
Sarah Johnson
Project Manager""",

    """Subject: Document Review Request

Hi John,

I've attached the quarterly report for your review. Could you please take a look and send me your feedback by Friday?

Let me know if you have any questions.

Thanks,
Mike""",

    """Subject: Meeting Rescheduled

Hello,

Our meeting originally scheduled for tomorrow at 2 PM has been rescheduled to next Monday at the same time.

Please let me know if this works for you.

Regards,
Lisa Chen""",

    # Personal emails
    """Subject: Dinner plans this weekend

Hey!

Are you free for dinner this Saturday? There's a new restaurant in Thamel I'd like to try.

Let me know what time works for you.

- Aayush""",

    """Subject: Thanks for your help

Hi Sita,

Thank you so much for helping me with the presentation yesterday. The client meeting went really well!

I owe you lunch.

Best,
Ramesh""",

    # Banking (legitimate)
    """Subject: Your Monthly Statement is Available

Dear Valued Customer,

Your monthly account statement for November 2024 is now available.

To view your statement:
1. Log in to your account at www.nepalbank.com.np
2. Navigate to Statements
3. Select November 2024

If you have any questions, please contact us at 01-4411234 or visit your local branch.

Thank you for banking with us.

Sincerely,
Customer Service Team
Nepal Bank Limited""",

    """Subject: Transaction Confirmation - Nepal Bank Limited

Dear Customer,

This email confirms your recent transaction:

Transaction Date: Nov 15, 2024
Amount: Rs. 4,599
Merchant: Daraz Nepal
Transaction ID: TXN123456789

If you have questions about this transaction, please contact our customer service at 01-4411234.

Thank you,
Nepal Bank Limited""",

    """Subject: Appointment Reminder

Dear Patient,

This is a reminder of your upcoming appointment:

Date: December 5, 2024
Time: 10:30 AM
Doctor: Dr. Sharma
Location: Nepal Cancer Hospital, Harisiddhi

Please arrive 15 minutes early to complete any necessary paperwork.

If you need to reschedule, please call us at 01-5522334.

Thank you,
Nepal Cancer Hospital""",

    # Service notifications
    """Subject: Order Shipped - Daraz Nepal

Hello,

Your order #ORD-789456 has been shipped!

Expected Delivery: Nov 20-22, 2024
Tracking Number: NPL123456789

You can track your package on our app or website: www.daraz.com.np

Thank you for shopping with Daraz!

Customer Service Team""",

    """Subject: Your Flight Confirmation - Buddha Air

Dear Passenger,

Your flight booking is confirmed:

Flight: Buddha Air U4 505
Route: Kathmandu (KTM) to Pokhara (PKR)
Date: December 1, 2024
Departure: 9:30 AM

PNR: ABCD123
Passenger: Ram Prasad Sharma

Please arrive at the airport 1 hour before departure.

Thank you for choosing Buddha Air.

Regards,
Buddha Air""",

    # ===== NEPALI LEGITIMATE EMAILS =====
    
    """विषय: साप्ताहिक बैठक - बिहीबार ३ बजे

नमस्कार टोली,

यो बिहीबार दिउँसो ३ बजे हाम्रो साप्ताहिक बैठक हुने सम्झना गराउँदछु।

एजेन्डा:
- परियोजना प्रगति
- प्रश्न र उत्तर
- आगामी योजना

कृपया तयारी गरेर आउनुहोस्।

धन्यवाद,
राम शर्मा
परियोजना प्रबन्धक""",

    """विषय: कागजात समीक्षा अनुरोध

नमस्कार,

मैले त्रैमासिक रिपोर्ट संलग्न गरेको छु। कृपया हेर्नुहोस् र शुक्रबार सम्म प्रतिक्रिया पठाउनुहोस्।

कुनै प्रश्न भए जानकारी गराउनुहोस्।

धन्यवाद,
सुरेश""",

    """विषय: बैठक समय परिवर्तन

नमस्कार,

भोलि दिउँसो २ बजे तोकिएको बैठक अबको सोमबार सोही समयमा सारिएको छ।

कृपया जानकारी गराउनुहोस्।

धन्यवाद,
गीता पौडेल""",

    """विषय: तपाईंको मासिक स्टेटमेन्ट उपलब्ध छ

प्रिय ग्राहक,

तपाईंको नोभेम्बर २०२४ को मासिक खाता स्टेटमेन्ट अब उपलब्ध छ।

स्टेटमेन्ट हेर्न:
१. www.nepalbank.com.np मा लग इन गर्नुहोस्
२. स्टेटमेन्ट खण्डमा जानुहोस्
३. नोभेम्बर २०२४ छान्नुहोस्

कुनै प्रश्न भए ०१-४४११२३४ मा सम्पर्क गर्नुहोस्।

धन्यवाद,
ग्राहक सेवा टोली
नेपाल बैंक लिमिटेड""",

    """विषय: लेनदेन पुष्टि - नेपाल बैंक लिमिटेड

प्रिय ग्राहक,

यो इमेलले तपाईंको हालको लेनदेन पुष्टि गर्दछ:

लेनदेन मिति: नोभेम्बर १५, २०२४
रकम: रु. ४,५९९
व्यापारी: दराज नेपाल
लेनदेन आईडी: TXN123456789

प्रश्न भए ०१-४४११२३४ मा सम्पर्क गर्नुहोस्।

धन्यवाद,
नेपाल बैंक लिमिटेड""",

    """विषय: अपोइन्टमेन्ट सम्झना

प्रिय बिरामी,

तपाईंको आउँदो अपोइन्टमेन्टको सम्झना:

मिति: डिसेम्बर ५, २०२४
समय: बिहान १०:३० बजे
डाक्टर: डा. शर्मा
स्थान: नेपाल क्यान्सर अस्पताल, हरिसिद्धि

कृपया १५ मिनेट अगावै आउनुहोस्।

पुन: निर्धारण गर्न ०१-५५२२३३४ मा फोन गर्नुहोस्।

धन्यवाद,
नेपाल क्यान्सर अस्पताल""",

    """विषय: तपाईंको सामान पठाइएको छ - दराज नेपाल

नमस्कार,

तपाईंको अर्डर #ORD-789456 पठाइएको छ!

अपेक्षित डेलिभरी: नोभेम्बर २०-२२, २०२४
ट्र्याकिंग नम्बर: NPL123456789

तपाईं आफ्नो प्याकेज www.daraz.com.np मा ट्र्याक गर्न सक्नुहुन्छ।

दराजमा किनमेल गर्नुभएकोमा धन्यवाद!

ग्राहक सेवा टोली""",

    """विषय: फ्लाइट पुष्टिकरण - बुद्ध एयर

प्रिय यात्री,

तपाईंको फ्लाइट बुकिङ पुष्टि भएको छ:

फ्लाइट: बुद्ध एयर U4 505
मार्ग: काठमाडौं (KTM) देखि पोखरा (PKR)
मिति: डिसेम्बर १, २०२४
प्रस्थान: बिहान ९:३० बजे

PNR: ABCD123
यात्री: राम प्रसाद शर्मा

कृपया प्रस्थान भन्दा १ घण्टा अगावै विमानस्थल आउनुहोस्।

बुद्ध एयर रोज्नुभएकोमा धन्यवाद।

सादर,
बुद्ध एयर""",

    """विषय: शैक्षिक कार्यक्रम जानकारी

प्रिय अभिभावक,

तपाईंको बच्चाको विद्यालयमा आगामी शैक्षिक कार्यक्रम हुने भएकोले जानकारी गराउँदछौं:

कार्यक्रम: वार्षिक खेलकुद प्रतियोगिता
मिति: मंसिर २५, २०८१
समय: बिहान ९ बजे देखि
स्थान: विद्यालय मैदान

अभिभावकहरूलाई कार्यक्रममा उपस्थित हुन अनुरोध गरिन्छ।

धन्यवाद,
प्रधानाध्यापक
शान्ति माध्यमिक विद्यालय""",

    """विषय: कार्यालय बन्द सूचना

सबै कर्मचारीहरूलाई सूचित गरिन्छ,

दशैं तथा तिहार २०८१ को अवसरमा कार्यालय निम्न मितिमा बन्द रहनेछ:

असोज २५ देखि कात्तिक १० सम्म

आवश्यक कामको लागि कात्तिक ११ गतेदेखि सम्पर्क गर्नुहोस्।

धन्यवाद,
प्रशासन विभाग""",

    # More mixed examples
    """Subject: Community Meeting Notice / सामुदायिक बैठक सूचना

Dear Residents / प्रिय बासिन्दाहरू,

There will be a community meeting next Sunday at 10 AM at the community hall.

आगामी आइतबार बिहान १० बजे सामुदायिक भवनमा बैठक हुनेछ।

Agenda / एजेन्डा:
- Waste management / फोहोर व्यवस्थापन
- Security issues / सुरक्षा मुद्दा
- Budget discussion / बजेट छलफल

Please attend / कृपया उपस्थित हुनुहोला।

Regards / सादर,
Community Committee / सामुदायिक समिति""",

]

# Calculate how many legitimate emails we need (same as phishing)
num_legitimate_needed = num_phishing

# If we don't have enough, duplicate and vary the existing ones
if len(legitimate_emails) < num_legitimate_needed:
    print(f"⚠️  Need {num_legitimate_needed} legitimate emails, but only have {len(legitimate_emails)}")
    print("   Duplicating and varying existing legitimate emails...")
    
    # Duplicate the list until we have enough
    while len(legitimate_emails) < num_legitimate_needed:
        legitimate_emails.extend(legitimate_emails[:min(len(legitimate_emails), num_legitimate_needed - len(legitimate_emails))])

# Trim to exact number needed
legitimate_emails = legitimate_emails[:num_legitimate_needed]

print(f"✅ Generated {len(legitimate_emails)} legitimate emails")

# 3. Create balanced dataset
print("\n" + "="*80)
print("CREATING BALANCED DATASET")
print("="*80)

# Create dataframe
balanced_data = {
    'email_text': phishing_emails + legitimate_emails,
    'label': [1] * num_phishing + [0] * len(legitimate_emails)
}

balanced_df = pd.DataFrame(balanced_data)

print(f"\n✅ Combined dataset created:")
print(f"   Total emails: {len(balanced_df)}")
print(f"   Phishing: {sum(balanced_df['label']==1)} ({sum(balanced_df['label']==1)/len(balanced_df)*100:.1f}%)")
print(f"   Legitimate: {sum(balanced_df['label']==0)} ({sum(balanced_df['label']==0)/len(balanced_df)*100:.1f}%)")

# Shuffle the dataset
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
print("✅ Dataset shuffled")

# 4. Save the balanced dataset
OUTPUT_PATH = "data/balanced_phishing_dataset.csv"
balanced_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')

print(f"\n✅ Balanced dataset saved to: {OUTPUT_PATH}")

# 5. Show samples
print("\n" + "="*80)
print("SAMPLE PREVIEW")
print("="*80)

print("\n📧 Sample PHISHING emails:")
for i in range(min(2, num_phishing)):
    print(f"\n{i+1}. {phishing_emails[i][:150]}...")

print("\n✅ Sample LEGITIMATE emails:")
for i in range(min(2, len(legitimate_emails))):
    print(f"\n{i+1}. {legitimate_emails[i][:150]}...")

print("\n" + "="*80)
print("🎉 DATASET CREATION COMPLETE!")
print("="*80)
print("\nNext step: Train the model with balanced data")
print("Run: python train_multi.py")
print("="*80)