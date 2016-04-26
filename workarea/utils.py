#!/usr/bin/python
# coding:utf8

import base64
import uuid
import hashlib
import datetime
import calendar
import random
import os.path

from pytz import timezone
# import pytz.utc as utc
from pytz import utc
from PIL import Image, ImageDraw, ImageFont, ImageFilter


FORMAT = "%Y-%m-%d"

def generate_cookie_secret():
    cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    return cookie_secret

def salt_password(salt, password):
    m = hashlib.md5()
    try:
        m.update(password)
    except:
        raise Exception("invalid password")
    m.update(salt)
    return m.hexdigest()

def get_cur_utc_timestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())

def get_today_date():
    return datetime.date.today().strftime(FORMAT)


def utc_timestamp_to_hk_datetime(timestamp):
    utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(timestamp))
    hk_tz = timezone("Asia/Hong_Kong")
    hk_dt = hk_tz.normalize(utc_dt.astimezone(hk_tz))
    return hk_dt

def gen_validate_code(width=100,
                      height=30,
                      mode="RGB",
                      bg_color=(0, 0, 0),
                      fg_color=(255, 255, 255),
                      font_size=18,
                      font_type="Ayuthaya.ttf",
                      length=4,
                      draw_points=True,
                      point_num = 75):
    image_size = (width, height)
    image = Image.new(mode, image_size, bg_color)
    draw = ImageDraw.Draw(image)

    def draw_code():
        new_strs = " ".join(strs)
        try:
            font = ImageFont.truetype(font_type, font_size)
        except:
            font_path = os.path.dirname(__file__) + "/static/font"
            file = "{}/{}".format(font_path, font_type)
            logging.info(file)
            font = ImageFont.truetype(file, font_size)
        strs_width, strs_height = font.getsize(new_strs)
        draw.text(((width - strs_width) / 2, (height - strs_height) / 2), new_strs,
                    font=font, fill=fg_color)

    def draw_points():
        """Draw disrupt points."""
        for _ in range(point_num):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point([x, y], fill=fg_color)


    population = "".join(map(str, range(10)))
    strs = "".join(random.sample(population, length))
    if draw_points:
        draw_points()
    draw_code()
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # strs = filter(lambda s: "0" < s < "9", strs)
    return image, strs

if __name__ == '__main__':
    # cookie_secret = generate_cookie_secret()
    # print cookie_secret
    gen_validate_code()

