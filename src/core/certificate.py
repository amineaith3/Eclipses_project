import os
from PIL import Image, ImageDraw, ImageFont
import datetime

class CertificateGenerator:
    @staticmethod
    def generate(name):
        try:
            # Create a high-quality certificate base
            width, height = 1200, 800
            img = Image.new('RGB', (width, height), color='#0f0f1a')
            draw = ImageDraw.Draw(img)
            
            # Draw decorative border
            draw.rectangle([20, 20, width-20, height-20], outline="#d4af37", width=10)
            draw.rectangle([40, 40, width-40, height-40], outline="#ffb74d", width=3)
            
            # Attempt to load fonts, fallback to default if not available
            try:
                title_font = ImageFont.truetype("arial.ttf", 60)
                sub_font = ImageFont.truetype("arial.ttf", 30)
                name_font = ImageFont.truetype("arial.ttf", 80)
            except IOError:
                title_font = ImageFont.load_default()
                sub_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                
            # Add logo if exists
            logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Astronest.png')
            if os.path.exists(logo_path):
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo = logo.resize((150, 150))
                    img.paste(logo, (int(width/2 - 75), 40), logo)
                except Exception:
                    pass
                
            # Text content
            draw.text((width/2, 220), "CERTIFICATE OF EXCELLENCE", font=title_font, fill="#d4af37", anchor="ms")
            draw.text((width/2, 320), "This certifies that", font=sub_font, fill="#aaaaaa", anchor="ms")
            draw.text((width/2, 450), name.upper(), font=name_font, fill="#ffffff", anchor="ms")
            draw.text((width/2, 550), "has achieved the prestigious title of", font=sub_font, fill="#aaaaaa", anchor="ms")
            draw.text((width/2, 650), "💎 DIAMOND RING MASTER 💎", font=title_font, fill="#ffb74d", anchor="ms")
            
            date_str = datetime.datetime.now().strftime("%B %d, %Y")
            draw.text((width/2, 720), f"Awarded on: {date_str} | Eclipse Explorer Q&A Pro", font=sub_font, fill="#777777", anchor="ms")
            
            # Save to Desktop
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            cert_path = os.path.join(desktop, "Eclipse_Certificate.png")
            img.save(cert_path)
            return cert_path
            
        except Exception as e:
            print("Failed to generate certificate:", e)
            return None
