#!/usr/bin/env python3

# Copyright 2017 generalrepo. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Main script. See README.md for more information

Use python 3
"""
#tutorial: https://docs.microsoft.com/en-us/azure/storage/storage-python-how-to-use-blob-storage
#pip install azure
from azure.storage.blob import BlockBlobService
if __name__ == "__main__":
    #Gets the blob service
    block_blob_service = BlockBlobService(account_name='mlpiano', account_key='AWsiStetr34ycMVEFkOznT3iORrmYA5P4cod5RkPMgh7VwW+GGktohnuwXqj/xccnSp71mWg4FViyGnB9/AUUg==')
    
    #Creates a blob called blobName from the file midi1.mid in container midiuploadrpi
    #block_blob_service.create_blob_from_path('midiuploadrpi', 'blobName', 'midi1.mid')

    #This line downloads a file from blob called blobName into the file test.mid
    #block_blob_service.get_blob_to_path('midiuploadrpi', 'blobName', 'test.mid')

    #Gets a list of blob info objects from the container midiuploadrpi
    generator = block_blob_service.list_blobs('midiuploadrpi')

    #Iterates through blob objects and gets the corresponding file from the storage service
    for blob in generator:
    	print(blob.name)
        #block_blob_service.get_blob_to_path('midiuploadrpi', blob.name, blob.name + '.mid')