//
//  UploadImageView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI
import PhotosUI
import Foundation

struct UploadImageView: View {
    @State var selectedItems: [PhotosPickerItem] = []
    @State var selectedItems2: [PhotosPickerItem] = []
    @State private var date = Date()
    @State private var date2 = Date()
    @State var data: Data?
    @State var data2: Data?

    var body: some View {
        VStack{
            if let data = data, let uiimage = UIImage(data: data){
                Image(uiImage: uiimage)
                    .resizable()
                    .frame(width: 256, height: 256)
            }
            PhotosPicker(selection: $selectedItems,
                         maxSelectionCount: 1,
                         matching: .images) {
                Text("Baseline Image")
            }
                         .onChange(of: selectedItems) { newValue in
                             guard let item = selectedItems.first else {
                                 return
                             }
                             item.loadTransferable(type: Data.self) {
                                 result in switch result{
                                 case .success(let data):
                                     if let data = data{
                                         self.data=data
                                     }
                                     else {
                                         print("Failure")
                                     }
                                 case .failure(let failure):
                                     fatalError("\(failure)")
                                 }
                             }
                         }
            DatePicker(
                    "Baseline Date",
                    selection: $date,
                    displayedComponents: [.date]
            ).padding([.leading, .trailing], 50)
            if let data = data2, let uiimage = UIImage(data: data){
                Image(uiImage: uiimage)
                    .resizable()
                    .frame(width: 256, height: 256)
            }
            PhotosPicker(selection: $selectedItems2,
                         maxSelectionCount: 1,
                         matching: .images) {
                Text("Progression Image")
            }
                         .onChange(of: selectedItems2) { newValue in
                             guard let item = selectedItems2.first else {
                                 return
                             }
                             item.loadTransferable(type: Data.self) {
                                 result in switch result{
                                 case .success(let data):
                                     if let data = data{
                                         self.data2=data
                                     }
                                     else {
                                         print("Failure")
                                     }
                                 case .failure(let failure):
                                     fatalError("\(failure)")
                                 }
                             }
                         }
            DatePicker(
                    "Progression Date",
                    selection: $date2,
                    displayedComponents: [.date]
                ).padding([.leading, .trailing], 50)
            Button("Upload Images", action: nUpload)
        }
    }

    func nUpload(){
        if let data = data, let uiimage = UIImage(data: data),
           let data2 = data2, let uiimage2 = UIImage(data: data2){
            sendImageToServer(image: uiimage, image2: uiimage2)
        }
    }
    func sendImageToServer(image: UIImage, image2: UIImage) {
        let url = URL(string: "http://10.197.59.173:5001/process_image")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Convert UIImage to Data
        guard let imageData = image.jpegData(compressionQuality: 1.0) else {
            print("Failed to convert UIImage to Data.")
            return
        }
        guard let imageData2 = image2.jpegData(compressionQuality: 1.0) else {
            print("Failed to convert UIImage to Data.")
            return
        }


        // Create multipart/form-data request
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        let httpBody = NSMutableData()
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMM_dd_Y"
        
        // Data for First Image
        httpBody.append("--\(boundary)\r\n".data(using: .utf8)!)
        httpBody.append("Content-Disposition: form-data; name=\"Image1\"; filename=\"\(dateFormatter.string(from: date)).jpg\"\r\n".data(using: .utf8)!)
        httpBody.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        httpBody.append(imageData)
        httpBody.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        
        //Data for Second Image
        httpBody.append("Content-Disposition: form-data; name=\"Image2\"; filename=\"\(dateFormatter.string(from: date2)).jpg\"\r\n".data(using: .utf8)!)
        httpBody.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        httpBody.append(imageData2)
        httpBody.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = httpBody as Data
        
        // Send the request
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            guard let data = data, error == nil else {
                print("Error sending image to server: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            // Handle response data from the server
            print("Response from server: \(String(data: data, encoding: .utf8) ?? "")")
        }
        task.resume()
    }
}

struct UploadImageView_Previews: PreviewProvider {
    static var previews: some View {
        UploadImageView()
    }
}
