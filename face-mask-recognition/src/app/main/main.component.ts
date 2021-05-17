import { Component, OnInit } from '@angular/core';
import { ImagePickerConf } from 'ngp-image-picker';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  onSelectFile(event: any) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      // reader.onload = (event: any) => {
      //     this.localUrl = event.target.result;
      // }
      reader.readAsDataURL(event.target.files[0]);
      console.log(reader)
  }
  }
}
