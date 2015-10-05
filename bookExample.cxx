#ifndef VTKM_DEVICE_ADAPTER
#define VTKM_DEVICE_ADAPTER VTKM_DEVICE_ADAPTER_SERIAL
#endif

#include <iostream>
#include <vtkm/cont/ArrayHandle.h>
#include <vtkm/cont/DeviceAdapterAlgorithm.h>
#include <vtkm/cont/internal/ArrayPortalFromIterators.h>
#include <vector>

#define SORT_SIZE 100

template< typename DeviceAdapter, typename T >
struct HelloWorld
{
  std::vector<vtkm::Float32> * InputData;
  vtkm::cont::ArrayHandle <vtkm::Float32> InputArray;

  void Initilize(std::vector<vtkm::Float32> * inputData)
  {
    this->InputData = inputData;

    vtkm::cont::ArrayHandle < vtkm::Float32 > tmpArray;
    tmpArray = vtkm::cont::make_ArrayHandle(*this->InputData);
    vtkm::cont::DeviceAdapterAlgorithm<DeviceAdapter>::Copy ( tmpArray ,this->InputArray);
  }

  void Sort(std::vector<vtkm::Float32> * outputData)
  {
    //Kick off sorting on execution environment
    vtkm::cont::DeviceAdapterAlgorithm<DeviceAdapter>::Sort(this->InputArray);

    typename vtkm::cont::ArrayHandle<T>::PortalControl readwritePortal = this->InputArray.GetPortalControl ();
    //Copy back results from execution environment to control environment
    std::copy(vtkm::cont::ArrayPortalToIteratorBegin(readwritePortal), vtkm::cont::ArrayPortalToIteratorEnd(readwritePortal), outputData->begin());
  }
};


typedef VTKM_DEFAULT_DEVICE_ADAPTER_TAG DeviceAdapter;
int main(int argc, char** argv)
{

  // Query which device we are currently running on
  typedef vtkm::cont::internal::DeviceAdapterTraits<DeviceAdapter> DeviceAdapterTraits;
  std::cout << "Running Hello World example on device adapter: "
            << DeviceAdapterTraits::GetId() << std::endl;

  //Initilize control/execution sorter with appropiate device adapter
  HelloWorld< DeviceAdapter, vtkm::Float32 > helloWorld;

  //Create an input vector to be sorted
  std::vector<vtkm::Float32> ReversedInput;
  ReversedInput.reserve( SORT_SIZE );
  for (int i = SORT_SIZE; i > 0; i-- )
  {
    ReversedInput.push_back( i );
  }

  // Initlize sorter with input vector
  helloWorld.Initilize(&ReversedInput);

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

