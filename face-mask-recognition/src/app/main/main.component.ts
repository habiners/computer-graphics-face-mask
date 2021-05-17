import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  imgUrl: string = "";
  verdict: JSON | undefined;
  ngOnInit(): void {
  }
  onSelectFile(event: any) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (eventer: any) => {
        console.log(eventer.target.result);
        this.imgUrl = eventer.target.result;
      };
      console.log(reader)
    }
  }

  async yeet(){
    console.log(this.imgUrl);
    // this.sentiment = await this.httpClient.get('http://127.0.0.1:5002/sentiment-analysis/' + this.cleaned).toPromise() as JSON;
    this.verdict = await this.httpClient.get('http://127.0.0.1:5002/mask-detector?imguri=' + this.imgUrl).toPromise() as JSON;
    // this.verdict = await this.httpClient.post('http://127.0.0.1:5002/mask-detector/' + this.imgUrl).toPromise() as JSON;
    console.log(this.verdict);
  }
}
