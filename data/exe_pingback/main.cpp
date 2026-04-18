#include <iostream>
#include <unistd.h>
#include <curl/curl.h>
#include "config.h"

size_t write_callback(char* content, size_t size, size_t nmemb, void* out) {
  ((std::string*) out)->append(content, size * nmemb);
  return size * nmemb;
}

CURLcode pingBack() {
  std::string buf;
  const char* url = (const char*) URL;
  curl_global_init(CURL_GLOBAL_DEFAULT);
  CURL* curl = curl_easy_init();
  curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0);
  curl_easy_setopt(curl, CURLOPT_URL, url);
  curl_easy_setopt(curl, CURLOPT_HTTPGET, 1);
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buf);
  CURLcode res = curl_easy_perform(curl);
  curl_easy_cleanup(curl);
  curl_global_cleanup();
  return res;
}

int main(int argc, char** argv) {
  CURLcode res = CURLE_OK;
  unsigned int retries = 0;
  while ((res = pingBack()) != CURLE_OK && retries < 5) {
    sleep(3);
    retries++;
  }
}
