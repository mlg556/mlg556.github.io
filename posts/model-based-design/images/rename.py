import pathlib as plib
import subprocess as sbp

images = plib.Path('.').glob("*")

for img in images:
    if img.suffix in [".PNG", ".JPG"]:
        cmd =["git", "mv", "-f", f"{img}", f"{img.stem}{img.suffix.lower()}"]
        # print(" ".join(cmd))
        sbp.check_call(cmd)