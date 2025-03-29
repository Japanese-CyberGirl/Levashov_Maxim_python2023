def merge_list_inplase(lst1, lst2):
    lst1+=[0 for _ in lst2]
    idx1=len(lst1)- len(lst2)-1
    idx2=len(lst2)-1
    idx3=len(lst1)-1
    while idx2>=0 :
        if idx1>=0 and lst1[idx1]>lst2[idx2]:
            lst1[idx3]=lst1[idx1]
            idx1-=1
        else:
            lst1[idx3]=lst2[idx2]
            idx2-=1
        idx3-=1
    return lst1

lst1=[1, 2, 5, 6, 8, 90]
lst2=[3, 4]

print(merge_list_inplase(lst1, lst2))

