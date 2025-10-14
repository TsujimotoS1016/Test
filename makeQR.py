import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

# QRコード作成
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=30,
    border=4,
)
qr.add_data("https://web-ext.u-aizu.ac.jp/circles/triathlon/minitora/minitora.html")  # ここを変更可能
qr.make(fit=True)

# 丸みを帯びたスタイルで画像生成
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    fill_color="Black",        # ドットの色（変更OK）
    back_color="white"        # 背景色（透明にもできる）
)

# 保存
img.save("rounded_qr.png")
