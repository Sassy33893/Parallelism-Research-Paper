
import time
import random
import math
import multiprocessing

#The following 2 functions were adapted from GeeksforGeeks (GeeksforGeeks, 2013)
def merge(arr, left, mid, right):
   n1 = mid - left + 1
   n2 = right - mid

   #Create temp arrays
   L = [0] * n1
   R = [0] * n2

   #Copy data to temp arrays L[] and R[]
   for i in range(n1):
       L[i] = arr[left + i]
   for j in range(n2):
       R[j] = arr[mid + 1 + j]

   i = 0
   j = 0
   k = left

   #Merge the temp arrays back
   # into arr[left..right]
   while i < n1 and j < n2:
       if L[i] <= R[j]:
           arr[k] = L[i]
           i += 1
       else:
           arr[k] = R[j]
           j += 1
       k += 1

   #Copy the remaining elements of L[], if there are any
   while i < n1:
       arr[k] = L[i]
       i += 1
       k += 1

   #Copy the remaining elements of R[], if there are any
   while j < n2:
       arr[k] = R[j]
       j += 1
       k += 1

#Sequential Merge Sort
def mergeSort(arr, left, right):
   if left < right:
       mid = (left + right) // 2
       mergeSort(arr, left, mid)
       mergeSort(arr, mid + 1, right)
       merge(arr, left, mid, right)


#Parallel merge sort

#pool.map only allows a function to have one argument, using a helper function works around this problem
def helperMergeSort(array):
   #run merge sort on the chunk and return it
   mergeSort(array,0,len(array)-1)
   return array


def ParallelMergeSort(arr, numProcessors):
   #split the initial array into chunks equivalent to the number of processors
   chunkSize = math.ceil(len(arr)/numProcessors)
   chunks = []

   i = 0
   while i < len(arr):
       chunk = arr[i:i+chunkSize]
       chunks.append(chunk)
       i += chunkSize

   #sort the chunks created in parallel
   with multiprocessing.Pool(processes=numProcessors) as pool:
       sortedChunks = pool.map(helperMergeSort, chunks)

   #the now sorted chunks are taken and merged into a single array which is then returned
   while len(sortedChunks) > 1:
       merged = []
       for i in range(0, len(sortedChunks), 2):
           if i+1 < len(sortedChunks):
               combined = sortedChunks[i] + sortedChunks[i+1]
               left = 0
               mid = len(sortedChunks[i]) - 1
               right = len(combined) - 1
               merge(combined,left, mid, right)
               merged.append(combined)
           else:
               merged.append(sortedChunks[i])
       sortedChunks = merged

   return sortedChunks[0]





if __name__ == "__main__":
   arraySizes = [50,500, 5000, 50000, 100000, 250000, 500000,1000000,2500000,5000000] #array sizes to be used
   numTrials = 10 #number of trials for each array size

   #running the test over different array sizes and outputting the average runtime over 10 trials
   for i in range(10):
       arraySize = arraySizes[i]
       print("Array Size:", arraySize)

       #generate random arrays
       trialArrays = []
       for i in range(numTrials):
           arr = []
           for j in range(arraySize):
               arr.append(random.randint(1,100000))
           trialArrays.append(arr)

       #Sequential Merge Sort
       print("Sequential")
       times = []
       for i in trialArrays:
           arrCopy = i.copy()  #make a copy of the array so that all runs within the same trial use the same array
           start = time.time()
           mergeSort(arrCopy,0, len(arrCopy)-1)
           times.append(time.time() -start)
       avgTime = sum(times)/numTrials
       print("Average Time:", avgTime)

       #Parallel Merge Sort
       for c in range(1, 4):  #run the same test for 2 cores, 4 cores, and 8 cores
           numProcessors = 2**c
           print("Cores:", numProcessors)
           times = []
           for i in trialArrays:
               arrCopy = i.copy()
               start = time.time()
               ParallelMergeSort(arrCopy, numProcessors)
               times.append(time.time()- start)
           avgTime = sum(times)/numTrials
           print("Average Time:", avgTime)

   print("End")



