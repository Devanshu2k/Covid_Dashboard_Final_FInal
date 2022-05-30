import torch
import torch.nn as nn
import torch.nn.functional as F # new 
def ClinicalPredict(X):
    class Net(nn.Module):

        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(26, 128)
            self.fc2 = nn.Linear(128, 4)

        def forward(self, x):
            #print(x)
            x = F.relu(self.fc1(x))
            x = F.softmax(self.fc2(x),-1)
            return x

    
    net = Net()
    net.load_state_dict(torch.load(r"E:\New folder\CovidDashboard_Final-main\final.pth"))
    B=[]
    for i,j in X.items():
        if i in ['Computed tomography (CT)','SARS-CoV-2 nucleic acids']:
            continue
        B.append(j)
    if(X['Computed tomography (CT)']==0):
        del X['Computed tomography (CT)']        
        B.append(0)
        B.append(1)
    else:
        del X['Computed tomography (CT)']
        B.append(1)
        B.append(0)
    if(X['SARS-CoV-2 nucleic acids']==0):
        del X['SARS-CoV-2 nucleic acids']
        B.append(1)
        B.append(0)
        B.append(0)
    elif(X['SARS-CoV-2 nucleic acids']== 1 or X['SARS-CoV-2 nucleic acids']==  2):
        del X['SARS-CoV-2 nucleic acids']
        B.append(0)
        B.append(1)
        B.append(0)
    else:
        del X['SARS-CoV-2 nucleic acids']
        B.append(0)
        B.append(0)
        B.append(1)
    means=[55.78090452261306,0.4914572864321608,37.687537688442085,335.08040201005025,30.875577889447246,92.11678391959818,36.542211055276404,122.49547738693467,3.9842311557788963,9.64693467336682,216.83115577889447,0.08013065326633168,0.4651155778894471,1.3357587939698474,4.321396984924626,0.33415075376884434,1.3900301507537653,7.983547738693462,24.351155778894455,65.9465427135679,6.227597989949749,0.7688442211055276,0.23115577889447236,0.5899497487437186,0.0371859296482412,0.37286432160804023]
    stds=[16.937280359662854, 0.5001784258449753, 1.0835079158729028, 10.905463891800666, 2.3531554530525507, 6.058730809557298, 5.896997081835589, 20.455544614630206, 0.6851681686639218, 1.39547203625785, 92.91736898408396, 0.116383649791144, 0.35655300021217684, 1.0385389162636705, 3.1039815993017386, 0.3799859117728046, 1.8860093549122108, 4.344531192682075, 12.68298128424042, 14.69407766474096, 3.365822593300694, 0.42178380757953365, 0.42178380757953365, 0.49208984134931333, 0.1893123227268433, 0.48380963951448913]
    pos=0
    print(len(B))
    for pos in range(len(means)):
        B[pos]=(B[pos]-means[pos])/stds[pos]
    B=torch.FloatTensor(B)
    predictions=net(B)
    o=0
    for m in predictions:
        if(m==max(predictions)):
            break
        o+=1
    
    if(o==0):
        return 'Mild conditions predicted,asymptotic'
    elif(o==1):
        return 'Suspective of Covid 19 if not,regular symptoms predicted'
    elif(o==2):
        return 'In control,supervision required'
    elif(o==3):
        return 'Immediate hospitalisation'