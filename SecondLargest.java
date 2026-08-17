public class SecondLargest {
    @SuppressWarnings("unused")
    int findSecondLargest(int[] arr) {
        int largest = arr[0];
        int secondLargest = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if(arr[i] > largest){
                largest = arr[i];
            }
        }
        for (int i = 0; i < arr.length; i++) {
            if(arr[i] > secondLargest && arr[i] < largest){
                secondLargest = arr[i];
            }
        }
        if(secondLargest == largest){
            return -1; 
        }
        return secondLargest;
    }
}
