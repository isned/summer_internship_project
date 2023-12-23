import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-edit-client',
  templateUrl: './edit-client.component.html',
  styleUrls: ['./edit-client.component.css']
})
export class EditClientComponent {
  updatedData: any;

  constructor(
    public dialogRef: MatDialogRef<EditClientComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private http: HttpClient
  ) {
    // Initialize updatedData with the data passed in
    this.updatedData = { ...data };
  }

  onSave() {
    // Call the API to update the customer data
    this.http.put(`http://localhost:5000/update_customer/${this.data.customerId}`, this.updatedData)
      .subscribe(
        (data) => {
          console.log(data);
          this.dialogRef.close('edited'); // Close the dialog
        },
        (error) => {
          console.error(error);
          // Handle error - log error details
        }
      );
  }

  onCancel() {
    this.dialogRef.close();
  }
}
