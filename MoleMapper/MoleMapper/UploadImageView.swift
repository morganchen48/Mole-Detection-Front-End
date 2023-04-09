//
//  UploadImageView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI
import PhotosUI

struct UploadImageView: View {
    @State var selectedItems: [PhotosPickerItem] = []
    @State var data: Data?

    var body: some View {
        VStack{
            if let data = data, let uiimage = UIImage(data: data){
                Image(uiImage: uiimage)
                    .resizable()
            }
            PhotosPicker(selection: $selectedItems,
                         maxSelectionCount: 1,
                         matching: .images) {
                Text("Photo Picker")
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
            Image(systemName: "camera")
                .font(.system(size:75))
            Button("Upload Image", action: nUpload)
        }
    }
    func uploadImage(){
        Task{
            await uploadImageAsync()
        }
    }
    func uploadImageAsync() async{
        guard let encoded = try? JSONEncoder().encode(convertImageToBase64String()) else {
            print("Failed to encode image")
            return
        }
        print("HELLO3")
        print(encoded)
        let url = URL(string: "http://10.197.59.173:5001/process_image")!
        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        
        do {
            let (data, _) = try await URLSession.shared.upload(for: request, from: encoded)
            // handle the result
        } catch {
            print("Checkout failed.")
        }

    }
    func convertImageToBase64String () -> String {
        if let data = data, let uiimage = UIImage(data: data){
            return uiimage.jpegData(compressionQuality: 1)?.base64EncodedString() ?? ""
        }
        return ""
    }
    
    func nUpload(){
        if let data = data, let uiimage = UIImage(data: data){
            sendImageToServer(image: uiimage)
        }
    }
    func sendImageToServer(image: UIImage) {
        let url = URL(string: "http://10.197.59.173:5001/process_image")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Convert UIImage to Data
        guard let imageData = image.jpegData(compressionQuality: 1.0) else {
            print("Failed to convert UIImage to Data.")
            return
        }
        
        // Create multipart/form-data request
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        let httpBody = NSMutableData()
        httpBody.append("--\(boundary)\r\n".data(using: .utf8)!)
        httpBody.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        httpBody.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        httpBody.append(imageData)
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
