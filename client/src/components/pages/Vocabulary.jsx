import { useRef, useState } from "react"
import { vocabC } from "../../funtions/Vocabulary"
import { useSelector } from "react-redux"

function Vocabulary() {
    const user = useSelector((state) => state.user.user)
    const [img, setImg] = useState(null)
    const [imgFile, setImgFile] = useState(null)
    const [imgd, setImgd] = useState(false)
    const inputRef = useRef()
    const [show, setshow] = useState(false)

    const handleChange = (e) => {
        const file = e.target.files[0]
        if (file) {
            setImg(URL.createObjectURL(file))
            setImgFile(file)
        }
    }

    const handleRemove = () => {
        setImg(null)
        setImgFile(null)
        setImgd(false)
        inputRef.current.value = ""
    }

    const handleSubmitCreate = async (e) => {
        e.preventDefault()
        try {
            const data = new FormData(e.currentTarget)
            if (imgFile) data.set("images", imgFile)

            const getform = {
                id: user.id,
                name: data.get("name"),
                read: data.get("read"),
                images: data.get("images")
            }
            const res = await vocabC(getform)
            console.log(res)
        } catch (err) {
            alert(err.response?.data?.detail || "เกิดข้อผิดพลาด")
        }
    }

    return (
        <div>
            <button className="absolute bottom-25 right-10 w-10 h-10 bg-pink-500 rounded-full justify-center items-center" onClick={() => setshow(true)}>
                +
            </button>
            <div>
                {show && (
                    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
                        onClick={() => setshow(false)}>
                        <div className="bg-white border-1 border-gray-500 p-4 rounded-2xl flex justify-center">
                            
                            <form onSubmit={handleSubmitCreate} className="flex flex-col gap-3 items-center">
                                <div className="flex flex-col items-center">
                                    <span className="font-serif text-2xl p-2" >E-Reading</span>
                                    <input className="w-64 border-1 border-gray-400 m-1 rounded-sm p-1" name="name" type="text" placeholder="ชื่อคำศัพท์" />
                                    <input className="w-64 border-1 border-gray-400 m-1 rounded-sm p-1" name="read" type="text" placeholder="คำอ่าน" />
                                </div>
                                <input
                                    type="file"
                                    ref={inputRef}
                                    className="hidden"
                                    accept="image/*"
                                    onChange={handleChange}
                                />
                                <div className=" flex w-100 h-32 justify-center">
                                    {img ? (
                                        <div
                                            style={{ backgroundImage: `url(${img})` }}
                                            onClick={() => setImgd(true)}
                                            className="w-32 h-32 rounded-xl bg-cover bg-center relative cursor-pointer "
                                        >
                                            {imgd && (
                                                <div className="absolute inset-0 bg-black/40 flex items-center justify-center gap-2">
                                                    <span
                                                        onClick={(e) => { e.stopPropagation(); setImgd(false) }}
                                                        className="text-white cursor-pointer"
                                                    >
                                                        ยกเลิก
                                                    </span>
                                                    <span
                                                        onClick={(e) => { e.stopPropagation(); handleRemove() }}
                                                        className="text-red-400 cursor-pointer"
                                                    >
                                                        ลบ
                                                    </span>
                                                </div>
                                            )}
                                        </div>
                                    ) : (
                                        <button
                                            type="button"
                                            onClick={() => inputRef.current.click()}
                                            className="w-32 h-32 rounded-xl border-2 border-dashed border-gray-300 
               hover:border-blue-400 hover:bg-blue-50
               flex flex-col items-center justify-center gap-2
               text-gray-400 hover:text-blue-400
               transition-all duration-200 cursor-pointer bg-white"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                                                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                                                />
                                            </svg>
                                            <span className="text-xs font-medium">เลือกรูปภาพ</span>
                                        </button>

                                    )}
                                </div>
                                <button type="submit">เพิ่มคำศัพท์</button>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Vocabulary