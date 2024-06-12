import os
import piexif
from PIL import Image


# 写一段1到100的累加和
def sum1to100():
    sum = 0
    for i in range(1, 101):
        sum += i
    print(sum)


def process_images_in_directory(directory,newimagedir_savepath):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".jpg"):
                image_path = os.path.join(root, file)
                print('image_path:', image_path)
                
                processed_image_path = remove_metadata(image_path,newimagedir_savepath)
                print('save file path:', processed_image_path)

def remove_metadata(image_path,newimage_path=''):
    image = Image.open(image_path)
    metadata = image.info
  # print('info', metadata)
  # 创建一个新的图像对象，只包含像素数据
    clean_image = Image.new(image.mode, image.size)
    
    clean_image.putdata(list(image.getdata()))
    
    # 准备元数据
    exif_dict = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}
    exif_dict["0th"][piexif.ImageIFD.Artist] = "Super恒得丰".encode('utf-8')
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = "https://hengdefeng99.com".encode('utf-8')
    # 将元数据添加到图像
    exif_bytes = piexif.dump(exif_dict)
  # 新图像的文件名称是旧图像名称加上_processed
    if(newimage_path==''):    
        new_image_name = image_path.split('.')[0] + "_processed." + image_path.split('.')[1]
    else:
        new_image_name = newimage_path+'/'+os.path.basename(image_path)
        
  #  print(new_image_name)  # 输出: old_image_processed.jpg
    clean_image.save(new_image_name,exif=exif_bytes)

    return new_image_name

print('输入要处理的图片文件夹:')
imagedir_path =input()
print('输入要保存的文件夹路径:')
newimagedir_savepath =input()

# Call the function with the desired directory
process_images_in_directory(imagedir_path,newimagedir_savepath)
print('处理完成')
# '/E:\Downloads\\baiduyun\\2024年春节图片\\处理后750-1083\\674934275')

