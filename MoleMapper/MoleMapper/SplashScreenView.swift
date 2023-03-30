//
//  SplashScreenView.swift
//  MoleMapper
//
//  Created by Morgan Chen on 3/30/23.
//

import SwiftUI

struct SplashScreenView: View {
    @State private var isActive = false
    @State private var size = 0.8
    @State private var opacity = 0.5
    var body: some View {
        if isActive{
            ContentView()
        }
        else{
            Color.black.ignoresSafeArea().overlay(
            VStack {
                VStack {
                    Image(systemName: "pill.fill")
                        .font(.system(size:50))
                        .foregroundColor(.red)
                    Text ("Mole Mapper")
                        .font (Font.custom( "Baskerville-Bold", size: 45))
                        .foregroundColor(.white.opacity(0.80))
                }
                .scaleEffect(size)
                .opacity (opacity)
                .onAppear {
                    withAnimation(.easeIn(duration: 1.2)) {
                        self.size = 0.9
                        self.opacity = 1.0
                    }
                }
            }
            .onAppear{
                DispatchQueue.main.asyncAfter(deadline:.now() + 2.0){
                    withAnimation{
                        self.isActive = true
                    }
                }
            })
        }
    }
}

struct SplashScreenView_Previews: PreviewProvider {
    static var previews: some View {
        SplashScreenView()
    }
}
