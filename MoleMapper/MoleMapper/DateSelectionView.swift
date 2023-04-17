//
//  DateSelectionView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI

struct StringList: Codable {
    var strings: [String]
}

class StringListViewModel: ObservableObject {
    @Published var strings = [String]()
    
    init() {
        guard let url = URL(string: "http://127.0.0.1:5000/strings") else { return }
        
        URLSession.shared.dataTask(with: url) { data, _, error in
            guard let data = data else { return }
            do {
                let decodedData = try JSONDecoder().decode(StringList.self, from: data)
                DispatchQueue.main.async {
                    self.strings = decodedData.strings
                }
            } catch {
                print("Error decoding JSON: \(error.localizedDescription)")
            }
        }.resume()
    }
}

struct DateSelectionView: View {
    @ObservedObject var viewModel = StringListViewModel()
    @State private var chosenDate: String = ""
    
    var body: some View {
        ZStack(){
            Color.orange.ignoresSafeArea()
            Text("Chosen Date: " + chosenDate)
                .position(x:200,y:15)
                .font(.system(size:25))
            Picker("Choose a Date to View", selection: $chosenDate) {
                ForEach(viewModel.strings, id: \.self) {
                    date in Text(date)
                }
            }.position(x:200,y:50)
            Text("Last Scan: ")
                .position(x:200, y:200)
                .font(.system(size: 25))
            if let link = "http://127.0.0.1:5000/" + chosenDate {
                AsyncImage(url: URL(string: link),content: { image in
                    image.resizable()
                         .aspectRatio(contentMode: .fit)
                         .frame(maxWidth: 300, maxHeight: 300)
                },
                           placeholder: {
                               ProgressView()
                           })
            }
        }
    }
}

struct DateSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        DateSelectionView()
    }
}
