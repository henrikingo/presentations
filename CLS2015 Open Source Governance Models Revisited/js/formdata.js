function TableData() {
    this.columns = [];
    this.data = [];
    this.id = "";
    this.orderBy = 0;
    this.order   = "ASC";
};

T = TableData.prototype;

T.addRow = function(newRow) {
  this.data.push(newRow);
  this.renderTable();
};


T.sort = function() {
  var orderBy = this.orderBy;
  var order   = this.order;
  this.data.sort( function(a, b) {
    if ( this.order == "ASC" ) {
      return a[orderBy] > b[orderBy];
    } else if ( this.order == "DESC" ) {
      return a[orderBy] < b[orderBy];
    }
  });
};

T.renderTable = function() {
  this.sort();
  
  var e = document.getElementById(this.id);
  
  var firstRow = '<tr>';
  for ( col in this.columns ) {
    firstRow = firstRow + '<th>' + this.columns[col] + '</th>';
  } 
  firstRow = firstRow + '</tr>';

  var dataRows = '';
  for ( row in this.data ) {  
    var aRow = '<tr>';
    for ( cell in this.data[row] ) {
      aRow = aRow + '<td>' + this.data[row][cell] + '</td>';
    } 
    aRow = aRow + '</tr>';
    dataRows = dataRows + aRow;
  }
  
  e.outerHTML = '<table id="' + this.id + '">' + firstRow + dataRows + '</table>'; 
};


