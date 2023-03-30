//
//  DateSelectionView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI

struct DateSelectionView: View {
    public let dates: [String] = [
        "January 12, 2021",
        "March 1, 2021",
        "October 1, 2021",
        "March 1, 2022",
        "December 3, 2022",
    ]
    var links = ["January 12, 2021" : "https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?cs=srgb&dl=pexels-evg-kowalievska-1170986.jpg&fm=jpg",
                 "March 1, 2021": "https://i.kym-cdn.com/entries/icons/mobile/000/031/003/cover3.jpg",
                 "October 1, 2021": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492__340.jpg",
                 "March 1, 2022": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Welchcorgipembroke.JPG/1200px-Welchcorgipembroke.JPG",
                 "December 3, 2022": "https://i.kym-cdn.com/photos/images/original/002/014/238/731.jpg",
    ]
    @State private var chosenDate: String = ""
    
    var body: some View {
        ZStack(){
            Color.orange.ignoresSafeArea()
            Text("Chosen Date: " + chosenDate)
                .position(x:200,y:15)
                .font(.system(size:25))
            Picker("Choose a Date to View", selection: $chosenDate) {
                ForEach(dates, id: \.self) {
                    date in Text(date)
                }
            }.position(x:200,y:50)
            Text("Last Scan: ")
                .position(x:200, y:250)
                .font(.system(size: 25))
            if let link = links[chosenDate] {
                AsyncImage(url: URL(string: link), scale: 5)
            }
        }
    }
}

struct DateSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        DateSelectionView()
    }
}
