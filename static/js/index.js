let grids = document.getElementsByClassName("grid-item");
for (let i = 0; i < grids.length; i++) {
    grids[i].addEventListener("click", function (e) {
        alert(this.id);
        alert(this.className);
    });
};


