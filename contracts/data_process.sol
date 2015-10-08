contract DataProcess {
  int256 trans_id;
  struct Trans {
    address user;
    address seller;
    bytes16 status;
    uint amount;
  }
  mapping (int256 => Trans) transes;
  function DataProcess(){
    trans_id = 0;
  }
  function registSeller() returns (int256 uid){
    int256 sid = trans_id++;
    Trans tr = transes[sid];
    tr.seller = msg.sender;
    tr.status = "idle";
    return sid;
  }
  function registBuyer(int256 sid) returns (bool re){
    Trans tr = transes[sid];
    if(tr.status == "idle"){
      tr.user = msg.sender;
      return true;
    }
    else
      return false;
  }
  function getStatus(int256 sid) returns (bytes16 p){
    Trans tr = transes[sid];
    return tr.status;
  }
  function callforProcess(int256 id){
    Trans tr = transes[id];
    if(msg.value >= 20000){
        tr.status = "processing...";
        tr.amount = msg.value;
    }
  }
  function finish(int256 id){
    Trans tr = transes[id];
    tr.status = "finished";
  }
  function confirm(int256 id){
    Trans tr = transes[id];
    tr.seller.send(tr.amount);
    tr.status = "idle";
  }
}