from django.shortcuts import render,redirect
import pickle
from django.utils.datastructures import MultiValueDictKeyError
import io
import base64
from PIL import Image
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from .models import Blog,CropInfo,PreviousCropPred,FertilizerInfo,PreviousFertilizerPred

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def crop(request):
    if request.method == 'POST':
        finalList = []
        try:
            finalList.append(float(request.POST["N"]))
            finalList.append(float(request.POST["P"]))
            finalList.append(float(request.POST["K"]))
            finalList.append(float(request.POST["temp"]))
            finalList.append(float(request.POST["hum"]))
            finalList.append(float(request.POST["ph"]))
            finalList.append(float(request.POST["rain"]))
        except MultiValueDictKeyError:
            finalList = []
        model = pickle.load(open("./models/Crop_LGBMClassifier.pkl", "rb"))
        # print("The Data is ===========> ", finalList)
        ans = model.predict([finalList])
        # print("The Ans is ===========> ", ans)
        cropDesc = CropInfo.objects.get(name__exact=ans[0])
        # print("-----------> ",cropDesc)

        n = float(request.POST["N"])
        p = float(request.POST["P"])
        k = float(request.POST["K"])
        temp = float(request.POST["temp"])
        hum = float(request.POST["hum"])
        phl = float(request.POST["ph"])
        rainMM = float(request.POST["rain"])
        cropPred = cropDesc.name

        pred, isCreated = PreviousCropPred.objects.get_or_create(nitrogen=n,phosphorous=p,potassium=k,temperature=temp,humidity=hum,ph=phl,rain=rainMM,crop=cropPred)
        if(isCreated):
            pred.save()

        prevCrops = PreviousCropPred.objects.all()
        # print("-------------> ",prevCrops)
        return render(request, "crop.html", {"ans": ans[0],"cropDesc":cropDesc,"prevCrops":prevCrops})
    else:
        prevCrops = PreviousCropPred.objects.all()
        return render(request, "crop.html", {"prevCrops":prevCrops})


def fertilizer(request):
    croptype_dict = {0: 'Barley', 1: 'Cotton', 2: 'Ground Nuts', 3: 'Maize', 4: 'Millets',
                     5: 'Oil seeds', 6: 'Paddy', 7: 'Pulses', 8: 'Sugarcane', 9: 'Tobacco', 10: 'Wheat'}
    soiltype_dict = {0: 'Black', 1: 'Clayey', 2: 'Loamy', 3: 'Red', 4: 'Sandy'}
    fertName_dict = {0: '10-26-26', 1: '14-35-14',
                     2: '17-17-17', 3: '20-20', 4: '28-28', 5: 'DAP', 6: 'Urea'}
    if request.method == 'POST':
        finalList = []
        try:
            finalList.append(float(request.POST["temp"]))
            finalList.append(float(request.POST["hum"]))
            finalList.append(float(request.POST["moisture"]))
            finalList.append(float(request.POST["soil"]))
            finalList.append(float(request.POST["crop"]))
            finalList.append(float(request.POST["N"]))
            finalList.append(float(request.POST["K"]))
            finalList.append(float(request.POST["P"]))
        except MultiValueDictKeyError:
            finalList = []
        model = pickle.load(open("./models/Fertilizer_classifier.pkl", "rb"))
        # print("The Data is ===========> ", finalList)
        ans = model.predict([finalList])
        # print("The Ans is ===========> ", ans)
        fertObj = FertilizerInfo.objects.get(name__exact=fertName_dict[ans[0]])
        n = float(request.POST["N"])
        p = float(request.POST["P"])
        k = float(request.POST["K"])
        temp = float(request.POST["temp"])
        hum = float(request.POST["hum"])
        mois = float(request.POST["moisture"])
        cropt = croptype_dict.get(int(request.POST["crop"]))
        soilt = soiltype_dict.get(int(request.POST["soil"]))
        fert, isCreated = PreviousFertilizerPred.objects.get_or_create(nitrogen=n,phosphorous=p,potassium=k,temperature=temp,humidity=hum,moisture=mois,soil=soilt,crop=cropt,fertilizer=fertName_dict[ans[0]])
        if(isCreated):
            fert.save()

        prevFertilizers = PreviousFertilizerPred.objects.all()
        # print("-------------> ",prevFertilizers)
        return render(request, "fertilizer.html", {"ans": fertName_dict[ans[0]],"fertObj":fertObj,"prevFertilizers":prevFertilizers})
    else:
        prevFertilizers = PreviousFertilizerPred.objects.all()
        return render(request, "fertilizer.html", {"prevFertilizers":prevFertilizers})


def plant(request):
    li = [
        "Apple___Apple_scab",
        "Apple___Black_rot",
        "Apple___Cedar_apple_rust",
        "Apple___healthy",
        "Blueberry___healthy",
        "Cherry_(including_sour)___Powdery_mildew",
        "Cherry_(including_sour)___healthy",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Corn_(maize)___healthy",
        "Grape___Black_rot",
        "Grape___Esca_(Black_Measles)",
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Grape___healthy",
        "Orange___Haunglongbing_(Citrus_greening)",
        "Peach___Bacterial_spot",
        "Peach___healthy",
        "Pepper,_bell___Bacterial_spot",
        "Pepper,_bell___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Raspberry___healthy",
        "Soybean___healthy",
        "Squash___Powdery_mildew",
        "Strawberry___Leaf_scorch",
        "Strawberry___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___healthy",
    ]
    if request.method == "POST":
        try:
            myfile = request.FILES["myFile"]
        except MultiValueDictKeyError:
            myfile = ""
        b64_img = base64.b64encode(myfile.read()).decode("ascii")
        img = Image.open(io.BytesIO(
            base64.decodebytes(bytes(b64_img, "utf-8"))))
        img.save("my-image.jpeg")
        img = image.load_img("my-image.jpeg", target_size=(224, 224))
        # print("IMG1:", img)
        img = image.img_to_array(img)
        # print("IMG2:", img)
        img = np.expand_dims(img, axis=0)
        # print("IMG3:", img)
        img = img / 255
        # print("IMG4:", img)
        model = load_model("./models/Plant_AlexNetModel.hdf5")
        print("Following is our prediction:")
        prediction = model.predict(img)
        d = prediction.flatten()
        j = d.max()
        for index, item in enumerate(d):
            if item == j:
                class_name = li[index]
        # print("Our Prediction", class_name)
        return render(request, "plant.html", {"ans": class_name})
    else:
        return render(request, "plant.html", {})

def blogs(request):
    blogs = Blog.objects.all()
    # print(blogs)
    return render(request,"blogs.html",{"blogs":blogs})

def view_blog(request,bid):
    # print(bid)
    blog = Blog.objects.get(pk=bid)
    return render(request,"viewBlog.html",{"blog":blog})


def submitBlog(request):
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        date = request.POST["date"]
        description = request.POST["description"]
        process = request.POST["process"]
        uses = request.POST["uses"]
        others = request.POST["others"]
        conclusion = request.POST["conclusion"]
        bImage = request.FILES["image"]
        b64_img = base64.b64encode(bImage.read()).decode("ascii")
        img = Image.open(io.BytesIO(
            base64.decodebytes(bytes(b64_img, "utf-8"))))
        img.save(f"./blog/blogs/image/{bImage}")
        bImage=f"blogs/image/{bImage}"
        # print("------------------------------->",bImage)

        latestBlog = Blog.objects.order_by(('bid'))
        latestBID = latestBlog[len(latestBlog)-1].bid + 1   
        # print("-------------------------------------------------> ",latestBlog[len(latestBlog)-1].bid)
        blog, isCreated = Blog.objects.get_or_create(bid=latestBID,name=title,category=category,date=date,description=description,process=process,uses=uses,others=others,conclusion=conclusion,images=bImage)
        if(isCreated):
            blog.save()

    return redirect('/blogs/')

def cropStateWise(request):
    crop_data = {
    "wheat":["Uttar Pradesh, Punjab, Haryana, Rajasthan, Madhya Pradesh, bihar"],
    "paddy":["West Bengal, Uttar Pradesh, Andhra Pradesh, Punjab, Tamil Nadu"],
    "barley":["Rajasthan, Uttar Pradesh, Madhya Pradesh, Haryana, Punjab"],
    "maize":["Karnataka, Andhra Pradesh, Tamil Nadu, Rajasthan, Maharashtra"],
    "bajra":["Rajasthan, Maharashtra, Haryana, Uttar Pradesh and Gujarat"],
    "copra":["Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Orissa, West Bengal"],
    "cotton":["Punjab, Haryana, Maharashtra, Tamil Nadu, Madhya Pradesh, Gujarat"],
    "masoor":["Uttar Pradesh, Madhya Pradesh, Bihar, West Bengal, Rajasthan"],
    "gram":["Madhya Pradesh, Maharashtra, Rajasthan, Uttar Pradesh, Andhra Pradesh & Karnataka"],
    "groundnut":["Andhra Pradesh, Gujarat, Tamil Nadu, Karnataka, and Maharashtra"],
    "arhar":["Maharashtra, Karnataka, Madhya Pradesh and Andhra Pradesh"],
    "sesamum":["Maharashtra, Rajasthan, West Bengal, Andhra Pradesh, Gujarat"],
    "jowar":["Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Gujarat"],
    "moong":["Rajasthan, Maharashtra, Andhra Pradesh"],
    "niger":["Andha Pradesh, Assam, Chattisgarh, Gujarat, Jharkhand"],
    "jute":["West Bengal , Assam , Orissa , Bihar , Uttar Pradesh"],
    "safflower":["Maharashtra, Karnataka, Andhra Pradesh, Madhya Pradesh, Orissa"],
    "soyabean":["Madhya Pradesh, Maharashtra, Rajasthan, Madhya Pradesh and Maharashtra"],
    "urad":["Andhra Pradesh, Maharashtra, Madhya Pradesh, Tamil Nadu"],
    "ragi":["Maharashtra, Tamil Nadu and Uttarakhand"],
    "sunflower":["Karnataka, Andhra Pradesh, Maharashtra, Bihar, Orissa"],
    "sugarcane":["Uttar Pradesh, Maharashtra, Tamil Nadu, Karnataka, Andhra Pradesh"]
    }
    if request.method=="POST":
        crop = request.POST["crop"]
        states = crop_data[crop]
        print("----------------------> ",states)
        return render(request,'crop-state-wise.html',{"states":states,"crop":crop})
    return render(request,'crop-state-wise.html',{})
