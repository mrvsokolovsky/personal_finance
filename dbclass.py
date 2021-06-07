from prog import Receipt
import cv2
from pyzbar.pyzbar import decode


def read_barcodes(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        # 3
        with open("barcode_result.txt", mode='w') as file:
            file.write(barcode_info)
    return frame


def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()

    receipt = init()
    prods = receipt.get_receipt()
    receipt.db_connect(prods)


def init():
    string = open('barcode_result.txt', 'r')
    stringy = string.read().split('&')
    old_date = stringy[0][2:10]
    date = old_date[-2:] + old_date[-4:-2] + old_date[:4]
    time = stringy[0][11:15]
    paid = stringy[1][2:]
    fn = stringy[2][3:]
    fd = stringy[3][2:]
    fpd = stringy[4][3:]
    string.close()
    receipt = Receipt(fn, fd, fpd, date, time, paid)
    return receipt


if __name__ == '__main__':
    main()