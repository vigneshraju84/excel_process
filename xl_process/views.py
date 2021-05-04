from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import pandas as pd
import json

def xl_process(request):
	
	if "GET" == request.method:
		return render(request, 'xl_process.html', {})
	else:
		exception_err=""
		if "excel_file" in request.FILES:
			excel_file = request.FILES["excel_file"]
			
			try: 

				#read selected excel file using pandas 
				df = pd.read_excel(excel_file)			
				for i, row_cells in df.iterrows(): 
				
					if str(df.at[i,'Address']) !="nan":
						#Set parameters for map api service
						parameters={
							"key":"dCHB0rHZqBEBvMuPwZpzXJedn5AlloQQ",
							"location":str(df.at[i,'Address'])
						}
						
						#Location API call
						get_api_val= requests.get("http://www.mapquestapi.com/geocoding/v1/address?",params=parameters)
						
						api_data = json.loads(get_api_val.text)['results']
						print(api_data[0]['locations'][0])
						#set latitude value in variable
						lat = api_data[0]['locations'][0]['latLng']['lat']
						
						#set longitude value in variable
						lng = api_data[0]['locations'][0]['latLng']['lng']
						
						#update dataframe colu
						df.at[i,'Latitude']=lat
						df.at[i,'Longitude']=lng
						
						file_dir_folder="xl_files/"
						
						#update excel file with updated data frame value
						writer = pd.ExcelWriter(file_dir_folder+str(excel_file))
						df.to_excel(writer,index=False)
						writer.save()
					
				messages.success(request, 'Latitude & Longitude details updated successfully')
				return redirect("/")
				
			except Exception as e:
				
				exception_err = e
				
				return render(request, 'xl_process.html', {"exception_err":str(exception_err)})
			
		else:
			return render(request, 'xl_process.html', {"common_error":"Please choose excel file and process"})
