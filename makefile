generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

limpeza:
	rm -r ./NFS/Complementares/*
	rm -r ./NFS/Dicts_original/*
	mv ./log/geral*.log .
	rm -r ./log/*
