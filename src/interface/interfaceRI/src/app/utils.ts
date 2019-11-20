export class Utilities {
    public static paramsObjToStr(paramObjs: any): string {
        let queryParams: string = ""
        Object.keys(paramObjs).forEach(key=>{
            if(queryParams!="") {
                queryParams += "&";
            }
            queryParams += `${key}=${paramObjs[key]}`;
        })
        return '?' + queryParams;
    }
}