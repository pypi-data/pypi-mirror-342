# IM_COOL_BOOY_QR/main.py
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import argparse
from colorama import Fore, init
from datetime import datetime
from colorama import Style

def main_function():
    print("This is the main_function.")

def create_qr_tool(data, logo_path, frame_color, qr_color, bg_color, text, frame_margin=40, text_color="black"):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

        try:
            logo = Image.open(logo_path).convert("RGBA")
        except Exception as e:
            print(Fore.RED + "⚠️ Error opening logo image: " + Fore.WHITE + str(e))
            return

        qr_width, qr_height = img.size
        logo_width, logo_height = logo.size

        max_logo_size = min(qr_width, qr_height) // 4
        if logo_width > max_logo_size or logo_height > max_logo_size:
            logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

        logo_width, logo_height = logo.size
        position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

        img.paste(logo, position, mask=logo.split()[3])

        frame_width = img.width + 2 * frame_margin
        frame_height = img.height + 2 * frame_margin
        frame_img = Image.new('RGB', (frame_width, frame_height), frame_color)

        frame_img.paste(img, (frame_margin, frame_margin))

        draw = ImageDraw.Draw(frame_img)
        draw.rectangle(
            [(frame_margin - 2, frame_margin - 2), (frame_width - frame_margin + 2, frame_height - frame_margin + 2)],
            outline="black", width=4
        )

        font_path = "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerifCondensed-Italic.ttf"
        font = ImageFont.truetype(font_path, 20)
        text_width, text_height = draw.textbbox((0, 0), text, font)[2:]
        text_x = (frame_width - text_width) // 2
        text_y = frame_height - text_height - 10
        draw.text((text_x, text_y), text, font=font, fill=text_color)

        attribution_text = "SL Android Official ™ - Tool developed by IM COOL BOOY"
        attribution_font = ImageFont.truetype(font_path, 11)
        attribution_width, attribution_height = draw.textbbox((0, 0), attribution_text, attribution_font)[2:]
        attribution_x = (frame_width - attribution_width) // 2
        attribution_y = frame_height - text_height - 40
        draw.text((attribution_x, attribution_y), attribution_text, font=attribution_font, fill=text_color)

        output_dir = "/storage/emulated/0/IM-COOL-BOOY-QR"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = os.path.join(output_dir, f"QR_BOOY_{timestamp}.png")
        frame_img.save(output_filename)

        print(Fore.BLUE + "✅ QR code processed successfully: " + Fore.WHITE + output_filename)
        print(Fore.BLUE + "✅ SL Android Official ™ - Tool developed by IM COOL BOOY")

    except Exception as e:
        print(Fore.RED + "❌ Error: " + Fore.WHITE + f"{e}")

def main():
    init(autoreset=True)
    print(Fore.CYAN + Style.BRIGHT + "\n🚀 Main function is starting...\n")

    parser = argparse.ArgumentParser(description="Generate a customizable QR Code")
    parser.add_argument('--data', required=True, help="Data for the QR code (e.g., URL)")
    parser.add_argument('--logo', required=True, help="Path to the logo image")
    parser.add_argument('--frame_color', default="#800080", help="Color of the frame (default: purple)")
    parser.add_argument('--qr_color', default="#800080", help="QR code fill color (default: purple)")
    parser.add_argument('--bg_color', default="#D8BFD8", help="QR code background color (default: light purple)")
    parser.add_argument('--text', required=True, help="Text to display below the QR code")
    parser.add_argument('--frame_margin', type=int, default=40, help="Margin around the QR code (default: 40)")
    parser.add_argument('--text_color', default="#800080", help="Color of the text (default: purple)")

    args = parser.parse_args()

    print(Fore.MAGENTA + Style.BRIGHT + "🎨 Generating QR Code with the following parameters:\n")
    print(Fore.MAGENTA + "  🔗 Data: " + Fore.WHITE + args.data)
    print(Fore.MAGENTA + "  🖼️ Logo: " + Fore.WHITE + args.logo)
    print(Fore.MAGENTA + "  🟪 Frame Color: " + Fore.WHITE + args.frame_color)
    print(Fore.MAGENTA + "  ◼️ QR Code Fill Color: " + Fore.WHITE + args.qr_color)
    print(Fore.MAGENTA + "  🖌️ Background Color: " + Fore.WHITE + args.bg_color)
    print(Fore.MAGENTA + "  ✍️ Text: " + Fore.WHITE + args.text)
    print(Fore.MAGENTA + "  📏 Frame Margin: " + Fore.WHITE + str(args.frame_margin))
    print(Fore.MAGENTA + "  🖍️ Text Color: " + Fore.WHITE + args.text_color + "\n")

    create_qr_tool(
        args.data,
        args.logo,
        args.frame_color,
        args.qr_color,
        args.bg_color,
        args.text,
        args.frame_margin,
        args.text_color
    )

if __name__ == "__main__":
    main()
