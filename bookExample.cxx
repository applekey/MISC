#ifndef VTKM_DEVICE_ADAPTER
#define VTKM_DEVICE_ADAPTER VTKM_DEVICE_ADAPTER_CUDA
#endif

#include <iostream>
#include <vtkm/cont/ArrayHandle.h>
#include <vtkm/cont/DeviceAdapterAlgorithm.h>
#include <vtkm/cont/internal/ArrayPortalFromIterators.h>
#include <vector>

#define SORT_SIZE 100

using namespace vtkm::cont;

template<typename T,typename DeviceAdapter = 
                    VTKM_DEFAULT_DEVICE_ADAPTER_TAG >
class HelloWorld
{
  public:
  std::vector<vtkm::Float32> * InputData;
  ArrayHandle <vtkm::Float32> InputArray;

  void Initilize(std::vector<vtkm::Float32> * inputData)
  {
    this->InputData = inputData;

    ArrayHandle < vtkm::Float32 > tmpArray;
    tmpArray = vtkm::cont::make_ArrayHandle(*this->InputData);
    DeviceAdapterAlgorithm<DeviceAdapter>::
                            Copy(tmpArray, this->InputArray);
  }

  void Sort(std::vector<vtkm::Float32> * outputData)
  {
    //Start sorting on execution environment
    DeviceAdapterAlgorithm<DeviceAdapter>::Sort(this->InputArray);

    //Copy results from execution environment to control environment

    typename ArrayHandle<T>::PortalConstControl readPortal =
      this->InputArray.GetPortalConstControl();

    for ( vtkm :: Id index = 0; index < readPortal.GetNumberOfValues(); index ++)
    {
      (*outputData)[index] = readPortal.Get(index);
    }
  }
};


typedef VTKM_DEFAULT_DEVICE_ADAPTER_TAG DeviceAdapter;
int main(int argc, char** argv)
{

  // Query which device we are currently running on
  typedef internal::DeviceAdapterTraits<DeviceAdapter> DeviceAdapterTraits;
  std::cout << "Running Hello World example on device adapter: "
  << DeviceAdapterTraits::GetId() << std::endl;

  //Initilize control/execution sorter with appropiate device adapter
  HelloWorld< DeviceAdapter, vtkm::Float32 > helloWorld;

  //Create an input vector to be sorted
  std::vector<vtkm::Float32> RandomInput;
  RandomInput.reserve( SORT_SIZE );
  for (int i = 0; i < SORT_SIZE; i++ )
  {
    RandomInput.push_back( rand() );
  }

  // Initialize sorter with input vector
  helloWorld.Initilize(&RandomInput);

  //Declare an output
  std::vector< vtkm::Float32> OutputData;
  OutputData.reserve( SORT_SIZE );

  //Run sorter on execution environment, once complete transfer
  //back to control environment
  helloWorld.Sort(&OutputData);

  //print the result on control environment
  for (int i = 0; i < SORT_SIZE; i++ )
  {
    printf(" %f\n ", OutputData[i]);
  }

}
