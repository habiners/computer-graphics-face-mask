import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  imgUrl: string | ArrayBuffer | null | undefined= "/assets/images/no-face.png";
  resultImgUrl: string = "/assets/images/empty.png";
  verdict: JSON | any | undefined;
  disableAnalyze: boolean = true;
  outputBorderColor: string = 'black';
  buttonColor: string = 'white';
  buttonCursor: string = 'default';
  ngOnInit(): void {
  }

  setSubmitStyle(mouseEvent: boolean) {
    this.buttonColor = mouseEvent ? 'white' : this.disableAnalyze ? 'white' : 'lightgreen'
  }

  onSelectFile(event: any) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (eventer: any) => {
        this.imgUrl = reader.result;
      };
      this.disableAnalyze = false;
      this.buttonColor = 'lightgreen'
      this.buttonCursor = 'pointer'
    }
  }

  async analyze(){
    let resultJSON: any;

    this.resultImgUrl = "/assets/images/placeholder.gif"
    this.outputBorderColor = 'grey'
    this.disableAnalyze = true
    this.buttonColor = 'white'
    this.buttonCursor = 'default'

    this.verdict = await this.httpClient.get('http://127.0.0.1:5002/mask-detector/' + this.imgUrl?.toString()).toPromise() as JSON

    if (this.verdict["result"]) {
      this.resultImgUrl = "/assets/images/check.png"
      this.outputBorderColor = 'darkgreen'
    }
    else {
      this.resultImgUrl = "/assets/images/cross.png"
      this.outputBorderColor = 'darkred'
    }
    this.disableAnalyze = false;
    this.buttonColor = 'lightgreen'
    this.buttonCursor = 'pointer'

    console.log(this.verdict["result"]);
  }
}
