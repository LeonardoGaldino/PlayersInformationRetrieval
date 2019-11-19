import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { FormsModule }        from '@angular/forms';
import { HttpModule } from '@angular/http';
import { SearchResultComponent } from './search-result/search-result.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';
import { RiServiceService } from './ri-service.service';
import { DataService } from './data.service';

@NgModule({
  declarations: [
    AppComponent,
    SearchResultComponent,
    HomeComponent,
  ],
  imports: [
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    HttpModule
  ],
  providers: [RiServiceService,DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
