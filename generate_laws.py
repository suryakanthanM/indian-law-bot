from fpdf import FPDF
import os

# Create data/raw if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "Indian Law Database - Official Reference", border=False, align="C")
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=11)

law_content = """
THE MOTOR VEHICLES ACT, 1988 & CENTRAL MOTOR VEHICLES RULES
Traffic Laws & Vehicle Operation:
1. Valid Digital Documents: Under the IT Act 2000 and the Central Motor Vehicles Rules (CMVR), driving licenses, RC (Registration Certificates), and Insurance policies presented in electronic form via official apps like DigiLocker or mParivahan are legally on par with physical documents. Traffic authorities cannot refuse softcopies presented through these specific sovereign platforms.
2. Drunk Driving: Section 185 of the Motor Vehicles Act stipulates that driving under the influence of alcohol (exceeding 30 mg per 100 ml of blood) is punishable by imprisonment up to 6 months and/or a fine up to Rs 10,000 for a first offense.
3. Mobile Phones: Driving while using a handheld mobile device is strictly prohibited. However, the use of mobile phones for navigation (where the device is mounted) is allowed.

FUNDAMENTAL RIGHTS (CONSTITUTION OF INDIA)
Part III of the Indian Constitution enumerates Fundamental Rights:
1. Article 14: Equality before law.
2. Article 19: Freedom of speech and expression, assembly, association, movement, residence, and profession.
3. Article 21: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.
4. Article 21A: Right to free and compulsory education for all children between 6 to 14 years.

THE INFORMATION TECHNOLOGY ACT, 2000
1. Section 66C: Punishment for identity theft.
2. Section 66D: Punishment for cheating by personation by using computer resources.
3. Section 67: Publishing or transmitting obscene material in electronic form is heavily penalized.
4. Validity of e-records: Section 4 dictates that where any law provides that information or any other matter shall be in writing, such requirement shall be deemed to be satisfied if it is rendered or made available in an electronic form.

BHARATIYA NYAYA SANHITA (Replacing IPC)
1. Murder (formerly Sec 302 IPC): Now falls under Section 103 of BNS.
2. Sedition: The specific provision of sedition has been repealed and replaced with acts endangering sovereignty, unity, and integrity of India (Section 152).
3. Self Defense: The right of private defense continues to exist and extends to causing death in specific circumstances like apprehension of death, grievous hurt, rape, or kidnapping.

CONSUMER PROTECTION ACT, 2019
1. E-commerce: Online platforms and sellers are now firmly under the ambit of consumer protection laws. E-commerce entities must disclose return, refund, and grievance redressal mechanisms.
2. Misleading Advertisements: The CCPA (Central Consumer Protection Authority) can impose fines up to Rs 10 Lakhs on manufacturers or endorsers for false or misleading advertisements.
"""

pdf.multi_cell(w=0, h=8, text=law_content)
pdf.output("data/raw/comprehensive_indian_laws.pdf")
print("Successfully generated data/raw/comprehensive_indian_laws.pdf")
