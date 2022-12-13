const imgSrc = {
    name: [],
    pathArray: [],

    buildPathArray: function() {
        for (let i = 1; i <= 211; i++) {
            tmp_str = "../sprites/" + i + ".png";
            this.pathArray.push(tmp_str);
            this.name.push(i.toString());
        }
        for (let i = 1000; i < 1008; i++) {
            tmp_str = "../sprites/" + i + ".png";
            this.pathArray.push(tmp_str);
            this.name.push(i.toString());
        }
        for (let i = 0; i < this.name.length; i++)
            PIXI.Assets.add(this.name[i], this.pathArray[i]);
    },
};

class image {
    constructor(path) {
        this.obj = new Image();
        this.obj.src = path;
        if (this.obj.height > TILE_SIZE || this.obj.width > TILE_SIZE)
            this.isForeground = true;
    }
}

const keyboard = {
    listen: function() {
        window.addEventListener("keydown", (e) => {
            server.msgToServer = {
                msg_type: "key_input",
                key: e.key,
            };
            if (server.connection)
                server.connection.send(JSON.stringify(server.msgToServer));
        });
    },
};