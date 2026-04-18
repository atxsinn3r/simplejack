#include <iostream>
#include <windows.h>

int main(int argc, char** argv) {
  std::cout << "Executing WinExec()" << std::endl;
  UINT r = WinExec("\\\\localhost@8080\\hello_world.exe", SW_SHOW);
  if (r == 2) {
    std::cout << "file not found" << std::endl;
  } else {
    std::cout << r << std::endl;
  }
  return 0;
}
