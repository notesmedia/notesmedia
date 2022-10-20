import os
import pdf2image



size = 20

def create_thumpnail(file="" , override = False):
    note_folder = "./static/notes"
    output_folder = "./static/thumpnails"
    
    if file == "":
        
        for item in os.listdir(note_folder) :
            output_file = item.replace(".pdf" , ".png")
            if output_file not in os.listdir(output_folder) or override == True:
                print("converting")
                image = pdf2image.convert_from_path( os.path.join(note_folder , item), size , last_page = 1 )[0]
                output_path = os.path.join(output_folder , output_file)
                image.save(f"{output_path}" ,"PNG" )
    else:
        print("creating single thumpnail")
        output_path = os.path.join(output_folder , file.replace(".pdf" , ".png"))
        image = pdf2image.convert_from_path(os.path.join(note_folder,file) , 30 , last_page = 1)[0]
        print("----------------------------------")
        print(image)
        image.save(output_path , "PNG")
        

if __name__ == "__main__":
    create_thumpnail(override= True)
    print("this is latest")
