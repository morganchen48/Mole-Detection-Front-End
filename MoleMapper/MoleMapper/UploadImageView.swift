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
            Text("Upload Image")
                .font(.system(size:25))
        }
        
        
    }

}

struct UploadImageView_Previews: PreviewProvider {
    static var previews: some View {
        UploadImageView()
    }
}
