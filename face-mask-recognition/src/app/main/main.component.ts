import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(private httpClient: HttpClient) { }

  imgUrl: string | ArrayBuffer | null | undefined= "";
  verdict: JSON | undefined;
  ngOnInit(): void {
  }

  onSelectFile(event: any) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = (eventer: any) => {
        this.imgUrl = reader.result;
      };
    }
  }

  async yeet(){
    this.verdict = await this.httpClient.get('http://127.0.0.1:5002/mask-detector/' + this.imgUrl?.toString()).toPromise() as JSON;
    console.log(this.verdict);
  }
}
