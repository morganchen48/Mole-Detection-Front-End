//
//  ContentView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI
struct ContentView: View {
    let buttonColor = Color(red: 0.97, green: 0.596, blue: 0.502)
    let backgroundColor = Color(red: 0, green: 1, blue: 1)
    var body: some View {
        NavigationView{
            ZStack{
                backgroundColor.ignoresSafeArea()
                VStack {
                    NavigationLink(destination: AcquireImageView()) {
                        HStack{
                            Image(systemName: "camera")
                                .font(.system(size:25))
                            Text("Start New Scan")
                                .font(.system(size:25))
                        }
                        .frame(width:250, height: 75, alignment: .center)
                        .background(buttonColor)
                        .cornerRadius(25)
                    }.navigationTitle("Home")
                    NavigationLink(destination: UploadImageView()) {
                        HStack{
                            Image(systemName: "square.and.arrow.up")
                                .font(.system(size:25))
                            Text("Upload Images")
                                .font(.system(size:25))
                        }
                        .frame(width:250, height: 75, alignment: .center)
                        .background(buttonColor)
                        .cornerRadius(25)
                    }
                    NavigationLink(destination: DateSelectionView()) {
                        HStack{
                            Image(systemName: "person.crop.rectangle.stack")
                                .font(.system(size:25))
                            Text("View Past Scans")
                                .font(.system(size:25))
                        }
                        .frame(width:250, height: 75, alignment: .center)
                        .background(buttonColor)
                        .cornerRadius(25)
                    }
                }
            }
        }
    }
}
        
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
