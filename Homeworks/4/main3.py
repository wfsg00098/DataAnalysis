import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

X = [653.33, 546.67, 563.33, 726.67, 830, 733.33, 646.67, 625, 650, 615, 575, 560, 756.67, 803.33, 560, 900, 616.67,
     685, 755, 586.67, 636.67, 596.67, 650, 593.33, 570, 623.33, 603.33, 560, 580, 1080, 630, 633.33, 563.33, 546.67,
     533.33, 480, 446.67, 380, 443.33, 740, 730, 660, 636.67, 593.33, 563.33, 553.33, 686.67, 646.67, 676.67, 570,
     603.33, 763.33, 673.33, 643.33, 673.33, 513.33, 493.33, 583.33, 666.67, 633.33, 555, 536.67, 703.33, 666.67,
     666.67, 520, 560, 545, 606.67, 606.67, 593.33, 530, 560, 530, 643.33, 633.33, 635, 676.67, 603.33, 595, 783.33,
     736.67, 953.33, 715, 645, 730, 713.33, 896.67, 783.33, 630, 613.33, 656.67, 720, 760, 700, 850, 846.67, 876.67,
     850, 716.67, 700, 726.67, 670, 680, 610, 696.67, 683.33, 580, 670, 645, 645, 730, 670, 696.67, 726.67, 670, 686.67,
     730, 720, 750, 640, 610, 620, 576.67, 580, 693.33, 630, 536.67, 510, 570, 640, 653.33, 706.67, 726.67, 713.33, 660,
     675, 680, 700, 710, 700, 710, 733.33, 683.33, 753.33, 713.33, 666.67, 656.67, 830, 836.67, 860, 720, 696.67, 590,
     796.67, 890, 505, 883.33, 840, 746.67, 550, 686.67, 663.33, 686.67, 743.33, 563.33, 536.67, 623.33, 596.67, 690,
     683.33, 1452.5, 726.67, 700, 716.67, 860, 770, 790, 796.67, 770, 756.67, 796.67, 703.33, 730, 673.33, 746.67, 660,
     683.33, 783.33, 856.67, 810, 725, 825, 636.67, 570, 580, 673.33, 616.67, 535, 593.33, 520, 600, 650, 663.33,
     646.67, 465, 623.33, 530, 450, 686.67, 736.67, 726.67, 710, 685, 670, 830, 840, 810]
Y = [670, 605, 610, 690, 805, 700, 635, 615, 635, 590, 550, 560, 730, 765, 555, 916.67, 583.33, 580, 655, 560, 590, 535,
     613.33, 543.33, 533.33, 625, 610, 525, 565, 1290, 590, 580, 480, 485, 530, 463.33, 440, 380, 385, 770, 680, 595,
     620, 573.33, 545, 540, 665, 646.67, 635, 540, 585, 580, 646.67, 605, 650, 515, 515, 540, 635, 610, 515, 530, 665,
     635, 655, 490, 520, 505, 580, 595, 610, 530, 525, 505, 630, 620, 645, 660, 595, 605, 763.33, 725, 890, 715, 615,
     733.33, 720, 756.67, 740, 580, 570, 630, 696.67, 760, 680, 850, 840, 835, 790, 670, 660, 715, 675, 700, 665, 600,
     595, 535, 600, 580, 610, 716.67, 695, 655, 700, 700, 685, 760, 740, 735, 600, 620, 630, 575, 655, 670, 645, 490,
     500, 503.33, 590, 615, 700, 720, 670, 645, 665, 670, 670, 670, 693.33, 700, 625, 655, 680, 693.33, 620, 645,
     776.67, 896.67, 903.33, 645, 680, 590, 730, 892, 540, 865, 865, 730, 690, 650, 670, 666.67, 700, 550, 535, 545,
     595, 665, 665, 1587.5, 686.67, 700, 685, 810, 750, 735, 760, 893.33, 726.67, 790, 720, 710, 625, 700, 680, 670,
     730, 770, 740, 660, 720, 626.67, 575, 575, 635, 585, 475, 595, 485, 470, 590, 580, 575, 500, 575, 525, 460, 680,
     665, 650, 655, 680, 685, 850, 786.67, 790]
Z = [225, 210, 195, 250, 335, 275, 225, 220, 215, 165, 165, 160, 255, 300, 175, 430, 200, 175, 220, 195, 216.67, 180,
      236.67, 186.67, 186.67, 225, 220, 170, 195, 441.67, 220, 215, 140, 140, 180, 145, 115, 60, 100, 295, 255, 200,
      210, 220, 200, 180, 245, 238.33, 220, 175, 180, 205, 256.67, 235, 258.33, 155, 180, 195, 220, 180, 145, 130, 230,
      235, 245, 120, 155, 145, 205, 225, 230, 155, 195, 180, 205, 215, 235, 225, 195, 215, 330, 315, 395, 235, 205,
      296.67, 301.67, 310, 288.33, 230, 200, 240, 251.67, 328.33, 241.67, 355, 345, 390, 340, 265, 245, 280, 240, 235,
      220, 195, 180, 140, 220, 195, 210, 283.33, 270, 250, 265, 270, 260, 285, 285, 290, 210, 230, 215, 190, 240, 255,
      235, 168.33, 175, 186.67, 200, 230, 270, 295, 235, 185, 240, 225, 250, 240, 255, 265, 245, 265, 275, 255, 241.67,
      240, 355, 421.67, 411.67, 205, 215, 135, 275, 364, 125, 310, 330, 250, 245, 250, 228.33, 243.33, 270, 150, 165,
      175, 205, 245, 250, 873.33, 283.33, 255, 270, 285, 285, 280, 308.33, 278.33, 261.67, 330, 285, 283.33, 225, 265,
      235, 250, 300, 315, 310, 255, 280, 220, 205, 210, 205, 180, 120, 185, 130, 135, 205, 195, 195, 145, 185, 170, 115,
      205, 235, 250, 175, 230, 235, 345, 310, 315]


x = []
y = []

MIN = 450
MAX = 900

for i in range(len(X)):
    if MIN<=Z[i]<=MAX:
        x.append(X[i])
        y.append(Y[i])

plt.scatter(x,y,marker='x')
plt.savefig('协作图'+str(MIN)+'-'+str(MAX)+'.png',dpi=1000)