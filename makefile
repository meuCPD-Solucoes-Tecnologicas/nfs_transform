generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base
